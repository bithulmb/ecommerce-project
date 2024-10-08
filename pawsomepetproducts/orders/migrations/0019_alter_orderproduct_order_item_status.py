# Generated by Django 4.2.14 on 2024-09-10 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0018_orderproduct_coupon_discount_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderproduct",
            name="order_item_status",
            field=models.CharField(
                choices=[
                    ("Processing", "Processing"),
                    ("Shipped", "Shipped"),
                    ("Delivered", "Delivered"),
                    ("Cancelled", "Cancelled"),
                    ("Returned", "Returned"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
