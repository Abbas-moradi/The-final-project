from django.db import models
from accounts.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category/%Y/%m/%d/', blank=True)
    status = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    is_child = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('product:category_filter', args=[self.slug,])

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    number = models.PositiveSmallIntegerField()
    available = models.BooleanField(default=True)
    discount = models.IntegerField()
    image = models.ImageField(upload_to='product/%Y/%m/%d/')
    created = models.DateTimeField(auto_now=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class ProductImage(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_img')
    image = models.ImageField(upload_to='product/%Y/%m/%d/')
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('product_id',)

    def __str__(self) -> str:
        return self.product_id


class Comment(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cmnt')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('product_id',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
