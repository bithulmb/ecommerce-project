from .models import Product,Product_Variant
from django.forms import ModelForm

class AddProductForm(ModelForm):
    class Meta:
        model = Product
        exclude=['slug']

class AddProductVariantForm(ModelForm):
    class Meta:
        model   = Product_Variant
        fields  =   "__all__"
