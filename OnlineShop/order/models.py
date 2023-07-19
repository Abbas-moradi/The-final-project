from django.db import models
from accounts.models import User
from product.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateField(auto_now=True)
    total_amount = models.IntegerField()
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('order_date',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self) -> str:
        return f'{self.user} - {self.order_date}'


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    item_total_amount = models.IntegerField()

    class Meta:
        ordering = ('order',)
        verbose_name = 'order item'
        verbose_name_plural = 'order items'

    def __str__(self) -> str:
        return f'{self.order} - {self.product}'