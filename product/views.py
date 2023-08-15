from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Category, Brand, Comment, ProductImage
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, CommentSerializer
from django.views import View
from django.http import HttpResponse
from order.forms import CartAddForm
from django.views.generic import ListView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from permissions import IsOwnerOrReadOnly
from order.models import Order, OrderItems
from django.shortcuts import get_object_or_404
from product.models import Comment


class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer(instance=queryset, many=True)
        return Response(serializer_class.data)


class Products(View):
    template_name = 'shop.html'

    @method_decorator(cache_page(60 * 15))
    def get(self, request, category_slug=None):
        form = CartAddForm()
        product_queryset = Product.objects.filter(available=True)
        serializer_class_product = ProductSerializer(instance=product_queryset, many=True)
        category_queryset = Category.objects.filter(is_child=False, status=True)
        serializer_class_category = CategorySerializer(instance=category_queryset, many=True)
        brand_queryset = Brand.objects.all()
        serializer_class_brand = BrandSerializer(instance=brand_queryset, many=True)
        
        if category_slug:
            category_queryset = Category.objects.get(slug=category_slug)
            product_queryset = product_queryset.filter(category=category_queryset)
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
    
class UserProfile(View):
    template_name = 'profile.html'

    def get(self, request):
        return render(request, self.template_name)
    

class SearchProduct(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'products'

    def get_queryset(self):
        search_products = self.request.GET.get('search_product')
        if search_products:
            products = Product.objects.filter(name__icontains = search_products)
            return products


class CommentView(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializers_data = CommentSerializer(instance=comments, many=True)
        return Response(serializers_data.data, status=status.HTTP_200_OK)

    def post(self, request):
        comment_data = CommentSerializer(data=request.data)
        if comment_data.is_valid():
            comment_data.save()
            return Response(comment_data.data, status=status.HTTP_201_CREATED)
        return Response(comment_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes = [IsOwnerOrReadOnly, ]
    def put(self, request, pk):
        comment_upd = Comment.objects.get(pk=pk)
        self.check_object_permissions(request, comment_upd)
        serializer_data = CommentSerializer(instance=comment_upd, data=request.data, partial=True)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = [IsOwnerOrReadOnly, ]
    def delete(self, request, pk):
        comment_dlt = Comment.objects.get(pk=pk)
        self.check_object_permissions(request, comment_dlt)
        comment_dlt.delete()
        return Response({'message': 'comment deleted...'}, status=status.HTTP_200_OK)
    
class ProductDetail(View):
    template_name = 'shop-details.html'

    def get(self, request, product_id):
        product_detail = Product.objects.filter(pk=product_id)
        img = ProductImage.objects.filter(product_id=product_id)
        comments = Comment.objects.filter(product_id=product_id, status=True)
        user_comment = None
        user_order = Order.objects.filter(user=request.user)
        if user_order.exists():
            user_order_item = OrderItems.objects.filter(order=user_order.first())
            # user_order_item = get_object_or_404(OrderItems, order=user_order)
            # user_order_item = OrderItems.objects.filter(order=user_order)
            if user_order_item:
                user_comment = True
            else:
                user_comment = False

        return render(request, self.template_name, {'product': product_detail, 'img': img, 'comment': user_comment, 'comments': comments})