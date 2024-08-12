from django.db import models
from accounts.models import CustomUser
from product.models import Product_Variant
# Create your models here.

class Cart(models.Model):
    cart_id     = models.CharField(max_length=250, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(f"cart for {self.cart_id}")

class CartItem(models.Model):
    
    cart        = models.ForeignKey(Cart,on_delete=models.CASCADE)
    variant     = models.ForeignKey(Product_Variant,on_delete=models.CASCADE)
    quantity    = models.PositiveIntegerField()
    is_active   = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.variant)
    
    def sub_total(self):
        return self.variant.price * self.quantity