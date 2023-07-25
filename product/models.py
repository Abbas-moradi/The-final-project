from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category/%Y/%m/%d/', blank=True)
    status = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    number = models.PositiveSmallIntegerField()
    available = models.BooleanField(default=True)
    discount = models.IntegerField()
    image = models.ImageField(upload_to='product/%Y/%m/%d/')
    created = models.DateTimeField(auto_now=True)
    brand = models.CharField(max_length=200)

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


class Comments(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cmnt')
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ('product_id',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'




