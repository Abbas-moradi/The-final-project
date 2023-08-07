from django.contrib import admin
from .models import Order, OrderItems


class OrderItemList(admin.TabularInline):
    model = OrderItems
    row_id_field = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_updated', 'paid')
    list_filter = ('paid',)
    inlines = (OrderItemList, )