from django.shortcuts import render, redirect
from django.views import View
from .forms import ContactForm
from OnlineShop import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
import logging
from order.models import OrderItems
from product.models import Product
from django.db.models import Count

"""
This view is responsible for displaying dynamic content on the homepage,
 including the most ordered product and the latest products. It calculates
   this information by querying the database and then renders the 
   'index.html' template with the appropriate data.
"""
class Home(View):
    template_name = 'index.html'

    def get(self, request):
        product_counts = OrderItems.objects.values('product').annotate(total_quantity=Count('product__id'))
        most_ordered_product = Product.objects.get(id=product_counts.order_by('-total_quantity').first()['product'])
        last_products = Product.objects.all().order_by('-id')[:2]
        return render(request, self.template_name, {'most_ordered_product': most_ordered_product, 'last_products': last_products})


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