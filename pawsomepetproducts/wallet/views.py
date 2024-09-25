from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Wallet

# Create your views here.

@login_required(login_url="login_page")
@never_cache
def user_wallet_view(request):

    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = wallet.transactions.all().order_by("-created_at")
    context = {
        "wallet": wallet,
        "transactions": transactions,
    }
    return render(request, "user_home/user_wallet.html", context)
