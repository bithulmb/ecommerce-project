from django import forms
from django.forms import ModelForm
from .models import Coupon


class ApplyCouponForm(forms.Form):
    code = forms.CharField(max_length=20)

class AddCouponForm(ModelForm):
    valid_from = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'text', 'class': 'datetimepicker'})
    )
    valid_to = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'text', 'class': 'datetimepicker'})
    )
    class Meta:
        model = Coupon
        fields = '__all__'
        # exclude = ['valid_from', 'valid_to']

    
    def clean_code(self):
        code = self.cleaned_data['code'].upper()  # Convert to uppercase for consistent checking

        # Check if a coupon with the same code (case insensitive) already exists
        if not self.instance.pk:
            if Coupon.objects.filter(code__iexact=code).exists():
                raise forms.ValidationError("A coupon with this code already exists. Please choose a different code.")

        return code
    
    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount < 1 or discount > 100:
            raise forms.ValidationError('Discount must be between 1% and 100%')
        return discount
    
    
    def clean_minimum_order_amount(self):
        minimum_order_amount = self.cleaned_data.get('minimum_order_amount')
        if minimum_order_amount < 0:
            raise forms.ValidationError('Minimum order amount must be a positive value.')
        return minimum_order_amount

    def clean_maximum_discount_limit(self):
        maximum_discount_limit = self.cleaned_data.get('maximum_discount_limit')
        if maximum_discount_limit is not None and maximum_discount_limit < 0:
            raise forms.ValidationError('Maximum discount limit must be a positive value.')
        return maximum_discount_limit
