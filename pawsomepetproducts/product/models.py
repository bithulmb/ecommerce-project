from django.db import models
from category.models import Category
from pet_type.models import PetType
from django.utils.text import slugify



# Create your models here.

class Product(models.Model):
    name        = models.CharField(max_length=60, unique=True)
    slug        = models.SlugField(max_length=60,unique=True, blank=True, null=True)
    description = models.TextField()
    pet_type    = models.ForeignKey(PetType, on_delete=models.CASCADE)
    category    = models.ForeignKey(Category,on_delete = models.CASCADE)
    is_active   = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    
    #overwriting save method to generate the slug while saving
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs) 


class Product_Variant(models.Model):
    product_name    = models.ForeignKey(Product, on_delete=models.CASCADE)
    size            = models.CharField(max_length=40, null=True)
    price           = models.DecimalField(max_digits=8, decimal_places=2)
    stock           = models.PositiveIntegerField()
    thumbnail       = models.ImageField(upload_to="photos/thumbnail_images", null=True)
    is_active       = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.product_name.name} {self.size}"
    


class Product_Images(models.Model):
    product_variant    = models.ForeignKey(Product_Variant, on_delete=models.CASCADE, null=True)
    images             = models.ImageField(upload_to="photos/product_images")

    def __str__(self) -> str:
        return f"image for {self.product_variant.product_name.name} "