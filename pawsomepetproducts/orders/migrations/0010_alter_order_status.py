# Generated by Django 4.2.14 on 2024-08-22 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0009_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Processing", "Processing"),
                    ("Shipped", "Shipped"),
                    ("Delivered", "Delivered"),
                    ("Cancelled", "Cancelled"),
                    ("Returned", "Returned"),
                ],
                default="Processing",
                max_length=20,
            ),
        ),
    ]
