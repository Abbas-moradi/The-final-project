from django.shortcuts import render
from django.views import View


class Cart(View):
    template_name = 'shopping-cart.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


class Checkout(View):
    template_name = 'checkout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass
