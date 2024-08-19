from django.db import models
from accounts.models import CustomUser
from product.models import Product_Variant

# Create your models here.


class Wishlist(models.Model):
        user            = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
        product_variant = models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
        added_at        = models.DateTimeField(auto_now_add=True)

        #added unique constraint to multiple fields user and product variant inorder to ensure no duplicate entries are created
        class Meta:
            constraints = [
                            models.UniqueConstraint(fields=['user', 'product_variant'], name='unique_wishlist_item')
        ]

        def __str__(self):
            return f"{self.user.first_name} - {self.product_variant.product_name} , {self.product_variant.size}"