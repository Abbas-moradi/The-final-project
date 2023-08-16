from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactForm
from OnlineShop import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
import logging


class Home(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass

class Contact(View):
    template_name = 'contact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['text']
            subject = 'contact us,'
            message = f'{name}\n{email}\n{message}'
            email_from = settings.EMAIL_HOST_USER
            try:
                send_mail(subject,message,email_from,["cafeshopproject098@gmail.com"],fail_silently=False,)
                return render(request, self.template_name)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
        else:
            print('form not valid...')
        return render(request, self.template_name)


class About(View):
    template_name = 'about.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass