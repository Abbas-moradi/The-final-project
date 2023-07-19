from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterationForm
import random
from utils import send_otp_code
from .models import OtpCode
from django.contrib import messages

class UserRegisterView(View):
    form_class = UserRegisterationForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
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
        return redirect('home:home')


class UserRegisterVerifyCodeView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass