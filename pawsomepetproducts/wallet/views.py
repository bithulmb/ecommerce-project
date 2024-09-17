from django.shortcuts import render

from .models import Wallet

# Create your views here.


def user_wallet_view(request):

    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = wallet.transactions.all().order_by("-created_at")
    context = {
        "wallet": wallet,
        "transactions": transactions,
    }
    return render(request, "user_home/user_wallet.html", context)
