from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from .managers import UserManager
from datetime import datetime, timedelta


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=13, unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    license_plate = models.PositiveSmallIntegerField()
    main_address = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('user',)
        verbose_name = 'address'
        verbose_name_plural = 'address'

    def __str__(self) -> str:
        return f'{self.user} from {self.province} - {self.city} - {self.street} - {self.license_plate}'


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=13)
    code = models.PositiveSmallIntegerField()
    created = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.phone_number} - {self.code} - {self.created}'
       

class Coupon(models.Model):
    code = models.CharField(max_length=20)
    discount = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    expire_day = models.SmallIntegerField(default=30)
    expire = models.DateField()
    used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.expire = datetime.now().date() + timedelta(days=self.expire_day)
        super(Coupon, self).save(*args, **kwargs)