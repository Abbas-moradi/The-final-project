from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Category
from .serializers import ProductSerializer
from django.views import View


class ProductCreateView(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer(instance=queryset, many=True)
        return Response(serializer_class.data)


class Products(View):
    template_name = 'shop-details.html'

    def get(self, request):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer(instance=queryset, many=True)
        return render(request, self.template_name, {"serializers": serializer_class.data})

