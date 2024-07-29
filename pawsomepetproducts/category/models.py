from django.db import models

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self) -> str:
        return self.name

