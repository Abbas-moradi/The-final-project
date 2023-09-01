# Generated by Django 4.2.2 on 2023-08-22 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_address_main_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('discount', models.IntegerField()),
                ('created', models.DateField(auto_now_add=True)),
                ('expire', models.DateField()),
            ],
        ),
    ]
