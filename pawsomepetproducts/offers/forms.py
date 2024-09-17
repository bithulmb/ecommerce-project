from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Min

from product.models import Product_Variant

from .models import CategoryOffer, ProductVariantOffer


class AddProductOffer(forms.ModelForm):
    class Meta:
        model = ProductVariantOffer
        fields = "__all__"

    def clean_discount_amount(self):
        discount_amount = self.cleaned_data.get("discount_amount")
        product = self.cleaned_data.get("product")

        if discount_amount is None:
            raise ValidationError("Discount amount is required.")

        if discount_amount <= 0:
            raise ValidationError("Discount amount must be positive.")

        if product and discount_amount > product.price:
            raise ValidationError(
                "Discount amount cannot be larger than the product price."
            )

        return discount_amount


class AddCategoryOffer(forms.ModelForm):

    class Meta:

        model = CategoryOffer
        fields = "__all__"

    def clean_discount_amount(self):
        discount_amount = self.cleaned_data.get("discount_amount")

        if discount_amount is None:
            raise ValidationError("Discount amount is required.")

        if discount_amount <= 0:
            raise ValidationError("Discount amount must be positive.")

        category = self.cleaned_data.get("category")
        if category:
            product_variants = Product_Variant.objects.filter(
                product_name__category=category
            )
            min_price = product_variants.aggregate(min_price=Min("price"))["min_price"]

            if min_price is not None and discount_amount >= min_price:
                raise ValidationError(
                    f"The discount amount should be less than the lowest product price (₹ {min_price}) in this category."
                )

        return discount_amount
