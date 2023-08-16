from rest_framework import serializers
from .models import Order, OrderItems


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

