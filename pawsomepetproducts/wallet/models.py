from django.db import models

from accounts.models import CustomUser

# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name}'s Wallet"


class WalletTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ("CREDIT", "CREDIT"),
        ("DEBIT", "DEBIT"),
    )

    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} "
