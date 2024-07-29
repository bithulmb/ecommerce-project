
from .models import PetType
from django.forms import ModelForm

class AddPetTypeForm(ModelForm):
    class Meta:
        model = PetType
        fields = "__all__"

