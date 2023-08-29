from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterationForm, VerifyForm, UserRegisterForm, UserLoginForm
import random
from OnlineShop import settings
from utils import send_otp_code
from .models import OtpCode, User, Address
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, OtpCodeSerializer, AddressSerializer
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddAddress, AddressSelectionForm
from order.models import *
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404


"""
This view handles the user registration process,
 including form validation, code generation, 
 and session management.
"""
class UserRegisterView(View):
    template_name = 'register.html'
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
    
        if form.is_valid():
            random_code = random.randint(10000, 99999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            print(random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'full_name': form.cleaned_data['full_name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'code sending for you')
            return redirect('accounts:verify_code')
        
        return render(request, 'verify.html', {'form':form})

"""
This view handles the code verification process during user
registration and creates a new user account upon successful verification.
It also manages error messages and redirects as needed.
"""
class UserRegisterVerifyCodeView(View):
    form_class = VerifyForm

    def get(self, request):
        form = self.form_class
        return render(request, 'verify.html', {'form':form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        otp_code_instance = OtpCode.objects.get(phone_number=user_session['phone'])
        form = VerifyForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            if int(cd['code']) == int(otp_code_instance.code):
                User.objects.create_user(
                    user_session['phone'],
                    user_session['email'],
                    user_session['full_name'],
                    user_session['password']
                )

                otp_code_instance.delete()

                messages.success(request, 'register success', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')
    
    
"""
These views handle user login and logout operations and provide
a seamless authentication process for users in my Django application.
"""
class UsreLoginView(View):
    form_class = UserLoginForm
    template_name = 'user_login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            phone = cd['phone']
            password = cd['password']
            user = authenticate(request, phone_number=phone, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:home')
            messages.error(request, 'phone or pass is wrong', 'warning')
        return render(request, self.template_name, {'form':form})

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('home:home')
            

class UserCreateView(APIView):

    def get(self, request):
        queryset = User.objects.all()
        serializer_class = UserSerializer(instance=queryset, many=True)
        return Response(serializer_class.data)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    
class UserAddress(View):
    template_name = 'address.html'
    form_class = AddAddress
    choice_address = AddressSelectionForm

    def get(self, request):
        user_address = Address.objects.filter(user=request.user)
        return render(request, self.template_name, {'form':self.form_class, 'user_address': user_address, 'choice_form': self.choice_address})
    
    def post(self, request):
        # user_address_exist = Address.objects.filter(user=request.user)
        # if user_address_exist:
        #     user_address_exist.delete()

        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Address.objects.create(
                user=request.user, province=cd['province'],
                city=cd['city'], street=cd['street'],
                license_plate=cd['license_plate']
                )
            return redirect('home:home')
        return render(request, self.template_name, {'form':self.form_class})
    

class ChoiceAddress(View):
    form_class = AddressSelectionForm

    def post(self, request):
        form = AddressSelectionForm(request.POST)
        address_id = form['address_id']
        if form.is_valid():
            user_addresses = Address.objects.filter(user=request.user)
            selected_address_id = form.cleaned_data['address_id']
            for address in user_addresses:
                if address.id == selected_address_id:
                    address.main_address = True
                    address.save()
                else:
                    address.main_address = False
                    address.save()
            return redirect('home:profile')
        return redirect('home:home')
    
class EditProfile(View):
    template = 'edit_profile.html'
    form = UserRegisterForm

    def get(self, request):
        current_user = request.user
        return render(request, self.template, {'form':self.form,'user':current_user})
    

class MyOrder(View):
    template_name = 'my_order.html'

    def get(self, request):
        user_order = Order.objects.filter(user=request.user)
        user_order_item = OrderItems.objects.filter(order__in=user_order)
        return render(request, self.template_name, {'orders':user_order, 'items':user_order_item})



"""
This UserViewSet provides a RESTful API for managing user data,
including creating, retrieving, updating, and deactivating user accounts.
It also enforces authentication for these operations, ensuring that only 
authenticated users can access these endpoints.
"""
class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()

    def list(self, request):
        serializer_data = UserSerializer(instance=self.queryset, many=True)
        return Response(data= serializer_data.data)

    def create(self, request):
        serializer_data = UserSerializer(data=request.POST)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer_data = UserSerializer(instance=user)
        return Response(data= serializer_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer_data = UserSerializer(instance=user, data=request.POST, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        user.is_active = False
        user.save()
        return Response({'result': 'user deactivated now...'}, status=status.HTTP_200_OK)
    