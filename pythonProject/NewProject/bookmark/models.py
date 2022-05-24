from django.db import models
from django.urls import reverse

class Bookmark(models.Model):

    site_name = models.CharField(max_length=200)
    url = models.URLField(verbose_name='Site URL')

    def __str__(self):
        return '이름:' + self.site_name + ', 주소(RUL) : ' + self.url

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id})