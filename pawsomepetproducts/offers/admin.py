from django.contrib import admin

from .models import CategoryOffer, ProductVariantOffer

# Register your models here.
admin.site.register(ProductVariantOffer)
admin.site.register(CategoryOffer)
