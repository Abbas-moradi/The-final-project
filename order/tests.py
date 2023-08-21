from django.test import TestCase
from django.test import TestCase
from django.utils import timezone
from accounts.models import User
from product.models import Product
from .models import Order, OrderItems
from django.test import TestCase
from django.urls import reverse, resolve
from . import views

class TestOrderUrls(TestCase):

    def test_cart_url_resolves(self):
        url = reverse('order:shopping-cart')
        self.assertEqual(resolve(url).func.view_class, views.CartView)

    def test_cart_add_url_resolves(self):
        product_id = 1
        url = reverse('order:cart_add', args=[product_id])
        self.assertEqual(resolve(url).func.view_class, views.CartAddView)

    def test_cart_del_url_resolves(self):
        product_id = 1
        url = reverse('order:cart_del', args=[product_id])
        self.assertEqual(resolve(url).func.view_class, views.CartDelView)

    def test_checkout_url_resolves(self):
        url = reverse('order:checkout')
        self.assertEqual(resolve(url).func.view_class, views.Checkout)


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(full_name='test_user')
        self.product = Product.objects.create(name='Test Product', price=10)

    def test_order_creation(self):
        order_date = timezone.now().date()
        total_amount = 100
        status = True
        order = Order.objects.create(user=self.user, order_date=order_date, total_amount=total_amount, status=status)
        
        self.assertIsInstance(order, Order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.order_date, order_date)
        self.assertEqual(order.total_amount, total_amount)
        self.assertEqual(order.status, status)

    def test_order_items_creation(self):
        order = Order.objects.create(user=self.user, order_date=timezone.now().date(), total_amount=100, status=True)
        quantity = 2
        item_total_amount = self.product.price * quantity
        order_item = OrderItems.objects.create(order=order, product=self.product, quantity=quantity, item_total_amount=item_total_amount)
        
        self.assertIsInstance(order_item, OrderItems)
        self.assertEqual(order_item.order, order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, quantity)
        self.assertEqual(order_item.item_total_amount, item_total_amount)



# email send by celery test

from django.test import TestCase
from django.core.mail import outbox
from .tasks import order_email_sender

class OrderEmailSenderTest(TestCase):
    def test_order_email_sender(self):
        order_id = 1
        user_email = 'en.moradi.66@gmail.com'

        order_email_sender.delay(order_id, user_email)

        self.assertEqual(len(outbox), 1)

        sent_email = outbox[0]
        self.assertEqual(sent_email.subject, 'The order was placed')
        self.assertEqual(sent_email.body, 'Your order 1 has been registered and is being tracked\nThis message has been sent to you by Abbas Moradi online shop')
        self.assertEqual(sent_email.from_email, 'en.moradi.66@gmail.com')
        self.assertEqual(sent_email.to, ['en.moradi.66@gmail.com'])
