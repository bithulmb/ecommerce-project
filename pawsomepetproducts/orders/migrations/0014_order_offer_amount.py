# Generated by Django 4.2.14 on 2024-08-31 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0013_alter_order_payment_method"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="offer_amount",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
