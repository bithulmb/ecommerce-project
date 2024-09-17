# Generated by Django 4.2.14 on 2024-09-03 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0014_order_offer_amount"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30, null=True)),
                ("address_line1", models.CharField(max_length=50)),
                ("address_line2", models.CharField(blank=True, max_length=50)),
                ("town", models.CharField(max_length=40)),
                ("city", models.CharField(max_length=40)),
                ("state", models.CharField(max_length=40)),
                ("pincode", models.CharField(max_length=10)),
                ("contact_number", models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="order_address",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="orders.orderaddress",
            ),
        ),
    ]
