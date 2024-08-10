from .models import Product,Product_Variant,Product_Images
from django.forms import ModelForm

class AddProductForm(ModelForm):
    class Meta:
        model = Product
        exclude=['slug']

class AddProductVariantForm(ModelForm):
    class Meta:
        model   = Product_Variant
        fields  =   "__all__"
        # exclude =['thumbnail']


class AddProductImages(ModelForm):
    class Meta:
        model   =Product_Images
        fields = ['images', 'is_active']
