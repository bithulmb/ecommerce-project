from django.contrib import admin
from .models import Product,Product_Images,Product_Variant,ReviewRating

# Register your models here.
admin.site.register(Product)
admin.site.register(Product_Images)
admin.site.register(Product_Variant)
admin.site.register(ReviewRating)

