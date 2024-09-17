from django.db import models
from django.db.models import Avg, Count
from django.utils.text import slugify

from accounts.models import CustomUser
from category.models import Category
from pet_type.models import PetType

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True, null=True)
    description = models.TextField()
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

    # overwriting save method to generate the slug while saving
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product_Variant(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=40, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_featured = models.BooleanField(default=False)
    popularity = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)

    thumbnail = models.ImageField(upload_to="photos/thumbnail_images", null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(f"{self.product_name.name} {self.size}")

    # function to findout the average rating of product
    def calculate_average_rating(self):
        reviews = ReviewRating.objects.filter(
            product_variant=self, status=True
        ).aggregate(average=Avg("rating"))
        return reviews["average"] or 0

    def count_review(self):
        reviews = ReviewRating.objects.filter(
            product_variant=self, status=True
        ).aggregate(count=Count("id"))
        count = 0

        if reviews["count"] is not None:

            count = int(reviews["count"])
        return count

    # function to calculatte the offer price based on product variant offer
    def get_offer_price(self):

        from offers.models import (  # impoerted inside the function to avoid circulat import
            CategoryOffer, ProductVariantOffer)

        original_price = self.price
        discount = 0

        # cheching if any product or category offer associated with the product
        variant_offer = ProductVariantOffer.objects.filter(
            product=self, is_active=True
        ).first()
        category_offer = CategoryOffer.objects.filter(
            category=self.product_name.category, is_active=True
        ).first()
        if variant_offer:
            discount = variant_offer.discount_amount
        if category_offer:
            if category_offer.discount_amount > discount:
                discount = category_offer.discount_amount

        offer_price = original_price - discount
        return offer_price

    def discount_amount(self):
        discount = 0
        variant_offer = self.variant_offer.filter(is_active=True).first()
        category_offer = self.product_name.category.category_offer.filter(
            is_active=True
        ).first()
        if variant_offer:
            discount = variant_offer.discount_amount
        if category_offer:
            if category_offer.discount_amount > discount:
                discount = category_offer.discount_amount

        return discount


class Product_Images(models.Model):
    product_variant = models.ForeignKey(
        Product_Variant, on_delete=models.CASCADE, related_name="images", null=True
    )
    images = models.ImageField(upload_to="photos/product_images")
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"image for {self.product_variant.product_name.name} "


class ReviewRating(models.Model):
    product_variant = models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user}- {self.product_variant} "

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product_variant.average_rating = (
            self.product_variant.calculate_average_rating()
        )
        self.product_variant.save()
