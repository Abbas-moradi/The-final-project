from django.db import models
from accounts.models import User
from product.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=True)
    order_updated = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('order_date',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self) -> str:
        return f'{self.user} - {self.order_date}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    price = models.IntegerField()

    class Meta:
        ordering = ('order',)
        verbose_name = 'order item'
        verbose_name_plural = 'order items'

    def __str__(self) -> str:
        return f'{self.order} - {self.product}'
    
    def get_cost(self):
        return self.price * self.quantity