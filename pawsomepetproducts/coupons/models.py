from django.db import models

# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # discount as a percentage
    minimum_order_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    maximum_discount_limit = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code