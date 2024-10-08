from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Product, Product_Images, Product_Variant, ReviewRating


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ["slug"]


class AddProductVariantForm(ModelForm):
    class Meta:
        model = Product_Variant

        exclude = ["average_rating", "popularity"]

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise ValidationError("Price must be a positive decimal value.")
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get("stock")
        if stock < 0:
            raise ValidationError("Stock must be a positive integer.")
        return stock


class AddProductImages(ModelForm):
    class Meta:
        model = Product_Images
        fields = [
            "images",
        ]


class ReviewForm(ModelForm):
    class Meta:
        model = ReviewRating
        fields = ["subject", "review", "rating"]
