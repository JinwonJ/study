from django.db import models

# Create your models here.
class Book(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField()
    url = models.URLField('url', unique=True)

    def __str__(self):
        return self.name