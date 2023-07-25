from django.shortcuts import render
from django.views import View
from product.models import Product


class Cart(View):
    template_name = 'shopping-cart.html'

    def get(self, request):
        product_in_order = request.COOKIES.get('cart')
        print(product_in_order)
        if product_in_order:
            product_ids = [int(product_id) for product_id in product_in_order.split(',')]
            products = Product.objects.filter(id__in=product_ids)
            print(product_ids)
        else:
            products = []
        return render(request, self.template_name, {'products': products})

    def post(self, request):
        pass


class Checkout(View):
    template_name = 'checkout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass
