from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from product.models import Product
from .cart import Cart
from .forms import CartAddForm
from accounts.models import Address



class CartView(View):
    template_name = 'shopping-cart.html'

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {'cart': cart})


class CartAddView(View):
    template_name = 'product:shop'

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart.add(product, quantity)
        return redirect(self.template_name)

class CartDelView(View):
    template_name = 'shopping-cart.html'

    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.dell(product)
        return redirect(self.template_name)


class Checkout(View):
    template_name = 'checkout.html'

    def get(self, request):
        cart = Cart(request)
        user_address = Address.objects.filter(user=request.user)
        if user_address:
            print('*'* 50)
            print('addres has exist...')
        else:
            return render(request, 'address.html')
        return render(request, self.template_name, {'cart': cart})


    def post(self, request):
        pass
