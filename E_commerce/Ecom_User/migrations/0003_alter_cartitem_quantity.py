# Generated by Django 5.1.3 on 2024-11-12 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecom_User', '0002_category_cart_notification_order_payment_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
