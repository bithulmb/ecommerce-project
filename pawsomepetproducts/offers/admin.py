from django.contrib import admin
from .models import ProductVariantOffer, CategoryOffer

# Register your models here.
admin.site.register(ProductVariantOffer)
admin.site.register(CategoryOffer)