from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from category.models import Category
from product.models import Product_Variant

# Create your models here.


class ProductVariantOffer(models.Model):
    product = models.ForeignKey(
        Product_Variant, on_delete=models.CASCADE, related_name="variant_offer"
    )
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.product_name} - ₹ {self.discount_amount}"


class CategoryOffer(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_offer"
    )
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category.name} - ₹ {self.discount_amount}"
