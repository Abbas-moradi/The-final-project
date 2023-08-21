from django.test import TestCase
from django.test import TestCase, RequestFactory
from django.urls import reverse
from .views import Products
from .models import Product, Category
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category, Brand, Comment, ProductImage, Order, OrderItems
from order.forms import CartAddForm


class ProductCreateViewTest(TestCase):
    def test_product_create_view(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        product = Product.objects.create(name='Test Product', price=100.0, available=True)
        url = reverse('product-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

class ProductsViewTest(TestCase):
    def test_products_view(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        product = Product.objects.create(name='Test Product', price=100.0, available=True)
        url = reverse('products')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_products_view_with_category(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        category = Category.objects.create(name='Test Category', slug='test-category')
        product = Product.objects.create(name='Test Product', price=100.0, available=True, category=category)

        url = reverse('products', args=['test-category'])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

class UserProfileViewTest(TestCase):
    def test_user_profile_view(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        order = Order.objects.create(user=user)

        url = reverse('user-profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order Date')

