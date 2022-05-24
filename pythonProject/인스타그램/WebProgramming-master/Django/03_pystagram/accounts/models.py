from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    profile_img_src = models.CharField(max_length=150, blank=True)
    profile_msg = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)