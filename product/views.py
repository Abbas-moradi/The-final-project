from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Category, Brand
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer
from django.views import View
from django.http import HttpResponse
from order.forms import CartAddForm


class ProductCreateView(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer(instance=queryset, many=True)
        return Response(serializer_class.data)


class Products(View):
    template_name = 'shop.html'

    def get(self, request, category_slug=None):
        print('*'*50)
        print(category_slug)
        form = CartAddForm()
        product_queryset = Product.objects.filter(available=True)
        serializer_class_product = ProductSerializer(instance=product_queryset, many=True)
        category_queryset = Category.objects.filter(is_child=False, status=True)
        serializer_class_category = CategorySerializer(instance=category_queryset, many=True)
        brand_queryset = Brand.objects.all()
        serializer_class_brand = BrandSerializer(instance=brand_queryset, many=True)
        if category_slug:
            category_queryset = Category.objects.get(slug=category_slug)
            product_queryset = product_queryset.get(category=category_queryset)
            serializer_class_product = ProductSerializer(instance=product_queryset, many=True)

        return render(request, self.template_name, {
            "serializers": serializer_class_product.data,
            "categories": serializer_class_category.data,
            "brands": serializer_class_brand.data,
            "form": form
            })


class ProductDetail(View):
    template_name = 'shop-details.html'

    def get(self, request):
        return render(request, self.template_name)