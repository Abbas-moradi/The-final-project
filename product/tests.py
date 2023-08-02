from django.test import TestCase
from django.test import TestCase, RequestFactory
from django.urls import reverse
from .views import Products
from .models import Product, Category

class TestProductsView(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(name='Test Product', category=self.category, available=True)

    def test_get_with_category_slug(self):
        url = reverse('shop')
        request = self.factory.get(url, {'category_slug': self.category.slug})
        response = Products.as_view()(request, category_slug=self.category.slug)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product', response.content)

    def test_get_without_category_slug(self):
        url = reverse('shop')
        request = self.factory.get(url)
        response = Products.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Product', response.content)

    def test_get_with_invalid_category_slug(self):
        url = reverse('shop')
        invalid_slug = 'invalid-slug'
        request = self.factory.get(url, {'category_slug': invalid_slug})
        response = Products.as_view()(request, category_slug=invalid_slug)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Test Product', response.content)

