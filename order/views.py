from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from product.models import Product
from .cart import Cart
from .forms import CartAddForm
from accounts.models import Address
from accounts.forms import AddAddress
from .models import Order, OrderItems
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import OrderSerializers, OrderItemSerializers
from rest_framework.permissions import IsAuthenticated
from django.core.mail import BadHeaderError, send_mail
from OnlineShop import settings
from django.http import HttpResponse
from order.tasks import order_email_sender



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
    form_class = AddAddress
    template_name = 'index.html'

    def get(self, request):
        cart = Cart(request)
        user_address = Address.objects.filter(user=request.user, main_address=True)
        
        if user_address:
            data_list = list(user_address.values())
            result_string = ""

            for data_dict in data_list:
                for value in data_dict.values():
                    result_string += str(value) + "-"
            order = Order.objects.create(
                user = request.user, paid = False,
                user_address = result_string
            )

            for item in cart:
                OrderItems.objects.create(
                    order=order, product=item['product'], 
                    quantity=item['quantity'], price=item['price']
                    )
                
            del request.session['cart']

            order_email_sender(order.id, request.user)
            # subject = 'The order was placed'
            # message = f'Your order {order.id} has been registered and is being tracked\nhis message has been sent to you by Abbas Moradi online shop'
            # email_from = settings.EMAIL_HOST_USER
            # try:
            #     send_mail(subject,message,email_from,[request.user],fail_silently=False,)
            order.paid = True
            order.save()
            return redirect('home:home')
            # except BadHeaderError:
            #     return HttpResponse("Invalid header found.")

        return render(request, 'address.html', {'form':self.form_class})
        

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = Order.objects.all()

    def list(self, request):
        serializer_data = OrderSerializers(instance=self.queryset.filter(user=request.user), many=True)
        return Response(data= serializer_data.data)

    def create(self, request):
        serializer_data = OrderSerializers(data=request.POST)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        serializer_data = OrderSerializers(instance=user)
        return Response(data= serializer_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        order = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        serializer_data = OrderSerializers(instance=order, data=request.POST, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(data= serializer_data.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        order = get_object_or_404(self.queryset.filter(user=request.user), pk=pk)
        order.is_active = False
        order.save()
        return Response({'result': 'order deleted now...'}, status=status.HTTP_200_OK)