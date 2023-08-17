from rest_framework import serializers
from .models import Product, Category, Brand, Comment


class ProductSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_comment(self, object):
        result = object.product_cmnt.all()
        return CommentSerializer(instance=result, many=True).data

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'