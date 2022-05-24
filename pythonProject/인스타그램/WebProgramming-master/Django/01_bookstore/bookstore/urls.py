from django.urls import re_path
from .views import *

app_name = 'bookstore'

urlpatterns = [
    re_path(r'^$', BookListView, name='list'),
    re_path(r'^(?P<code>b\d+)/$', BookDetailView, name='detail'),
]