from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterationForm, VerifyCodeForm
import random
from OnlineShop import settings
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, OtpCodeSerializer, AddressSerializer


class UserRegisterView(View):
    form_class = UserRegisterationForm
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
            random_code = random.randint(10000, 99999)
            send_otp_code(form.changed_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.changed_data['phone_number'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.changed_data['phone_number'],
                'emai': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'code sending for you')
            return redirect('accounts:verify_code')
        return render(request, 'verify.html', {'form':form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form':form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        otp_code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == otp_code_instance.code:
                User.objects.create_user(
                    user_session['phone_number'],
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
    

# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# def authenticate_user(request):
#     try:
#         email = request.data['email']
#         password = request.data['password']
#         user = User.objects.get(email=email, password=password)
#         if user:
#             try:
#                 payload = jwt_payload_handler(user)
#                 token = jwt.encode(payload, settings.SECRET_KEY)
#                 user_details = {}
#                 user_details['name'] = "%s %s" % (
#                     user.first_name, user.last_name)
#                 user_details['token'] = token
#                 user_logged_in.send(sender=user.__class__,
#                                     request=request, user=user)
#                 return Response(user_details, status=status.HTTP_200_OK)
#             except Exception as e:
#                 raise e
#         else:
#             res = {
#                 'error': 'can not authenticate with the given credentials or the account has been deactivated'}
#             return Response(res, status=status.HTTP_403_FORBIDDEN)
#     except KeyError:
#         res = {'error': 'please provide a email and a password'}
#         return Response(res)