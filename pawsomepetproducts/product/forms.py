from .models import Product
from django.forms import ModelForm

class AddProductForm(ModelForm):
    class Meta:
        model = Product
        exclude=['slug']
