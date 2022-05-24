from django.db import models


class User(models.Model):
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    pass
