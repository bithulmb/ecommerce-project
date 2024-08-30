from django.db import models
from accounts.models import CustomUser,Address
from product.models import Product,Product_Variant
from coupons.models import Coupon



# Create your models here.
class Payment(models.Model):
    user            = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    payment_id      = models.CharField(max_length=50)
    payment_method  = models.CharField(max_length=50)
    amount_paid     = models.CharField(max_length=50)
    status          = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model): 

    STATUS = (
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Returned', 'Returned'),
     
    )
    PAYMENT_METHODS=(
        ('Online','Online'),
        ('Cash On Delivery', 'Cash On Delivery')
    )
    user            = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    payment_method  = models.CharField(max_length=30, choices=PAYMENT_METHODS, null=True)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    address         = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    order_number    = models.CharField(max_length=20)
   
    total_amount    = models.DecimalField(max_digits=8, decimal_places=2)
    status          = models.CharField(max_length=20, choices=STATUS, default='Processing')
    is_ordered      = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    coupon          = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    order_total     = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    shipping_charge = models.DecimalField(max_digits=8, decimal_places=2, null = True)
    
    def __str__(self):
        return self.order_number
    
class OrderProduct(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True,)
    product = models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    product_price = models.DecimalField(max_digits=8,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return str(self.product.product_name) 
    
    
    def subtotal(self):
        return self.product_price*self.quantity 