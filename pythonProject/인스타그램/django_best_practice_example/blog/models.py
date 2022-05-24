from django.db import models
from django.conf import settings


class OwnedModel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True


class Post(OwnedModel):
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
