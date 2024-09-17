from django.db import models

# Create your models here.


class PetType(models.Model):
    name = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
