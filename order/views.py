from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from product.models import Product
from .cart import Cart
from .forms import CartAddForm
from accounts.models import Address
from accounts.forms import AddAddress
from .models import Order, OrderItems



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
    template_name = 'order:shopping-cart'

    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.dell(product)
        return redirect(self.template_name)


class Checkout(View):
    template_name = 'checkout.html'
    form_class = AddAddress

    def get(self, request):
        return render(request, self.template_name)


class Paid(View):

    def get(self, request):
        print('post method')
        cart = Cart(request)
        user_address = Address.objects.filter(user=request.user)
        data_list = list(user_address.values())
        result_string = ""
        for data_dict in data_list:
            for value in data_dict.values():
                result_string += str(value) + "-"
        if user_address:
            order = Order.objects.create(
                user = request.user, paid = True,
                user_address = result_string
            )
            for item in cart:
                OrderItems.objects.create(
                    order=order, product=item['product'], 
                    quantity=item['quantity'], price=item['price']
                    )
            del request.session['cart']
            return render(request, 'index.html')
        return render(request, 'address.html', {'form':self.form_class})
        

