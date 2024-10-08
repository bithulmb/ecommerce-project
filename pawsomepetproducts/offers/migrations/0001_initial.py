# Generated by Django 4.2.14 on 2024-08-31 14:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product", "0009_alter_reviewrating_review_alter_reviewrating_subject"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductVariantOffer",
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
                    "discount_percent",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="variant_offer",
                        to="product.product_variant",
                    ),
                ),
            ],
        ),
    ]
