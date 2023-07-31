from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.views import View
from django.http import HttpResponse


class ProductCreateView(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer(instance=queryset, many=True)
        return Response(serializer_class.data)


class Products(View):
    template_name = 'shop.html'

    def get(self, request):
        product_queryset = Product.objects.filter(available=True)
        serializer_class_product = ProductSerializer(instance=product_queryset, many=True)
        category_queryset = Category.objects.all()
        serializer_class_category = CategorySerializer(instance=category_queryset, many=True)
        return render(request, self.template_name, {
            "serializers": serializer_class_product.data,
            "categories": serializer_class_category.data
            })


class ProductDetail(View):
    template_name = 'shop-details.html'

    def get(self, request):
        return render(request, self.template_name)