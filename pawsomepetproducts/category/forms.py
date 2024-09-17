from django.forms import ModelForm

from .models import Category


class AddCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
