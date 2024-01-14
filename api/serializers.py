from rest_framework import serializers
from accounts.models import User, Address
from order.models import Order, OrderItems
from product.models import Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
    

    def validate_full_name(self, value):
        if 'admin' in value:
            raise serializers.ValidationError('Admin should not be in the full name')
        

class AddressSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        model = Address
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_order_items(self, object):
        result = object.items.all()
        return OrderItemSerializers(instance=result, many=True).data


class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only = True, slug_field='full_name')
    product_id = serializers.SlugRelatedField(read_only = True, slug_field='name')

    class Meta:
        model = Comment
        fields = '__all__'


