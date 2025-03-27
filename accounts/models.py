from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    doljnost_kg = models.CharField(max_length=255, null=True)
    doljnost_ru = models.CharField(max_length=255, null=True)
    doljnost_en = models.CharField(max_length=255, null=True)

    kafedra_kg = models.CharField(max_length=255, null=True)
    kafedra_ru = models.CharField(max_length=255, null=True)
    kafedra_en = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.username