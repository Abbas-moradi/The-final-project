# Generated by Django 4.2.2 on 2023-08-09 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_user_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]