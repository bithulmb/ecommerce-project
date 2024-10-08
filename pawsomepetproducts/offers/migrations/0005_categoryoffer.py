# Generated by Django 4.2.14 on 2024-08-31 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0001_initial"),
        ("offers", "0004_remove_productvariantoffer_discount_percent"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoryOffer",
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
                (
                    "discount_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=5),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="category_offer",
                        to="category.category",
                    ),
                ),
            ],
        ),
    ]
