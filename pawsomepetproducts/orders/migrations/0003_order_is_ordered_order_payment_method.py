# Generated by Django 4.2.14 on 2024-08-15 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_remove_order_ip_remove_order_is_ordered"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="is_ordered",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="order",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("Online", "Online"),
                    ("Cash On Delivery", "Cash On Delivery"),
                ],
                max_length=30,
                null=True,
            ),
        ),
    ]
