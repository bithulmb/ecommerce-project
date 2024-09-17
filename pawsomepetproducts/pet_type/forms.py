from django.forms import ModelForm

from .models import PetType


class AddPetTypeForm(ModelForm):
    class Meta:
        model = PetType
        fields = "__all__"
