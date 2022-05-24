from django.urls import re_path
from . import views

app_name = 'bookmark'

urlpatterns = [
    re_path(r'^$', views.BookmarkListView, name='list'),
    re_path(r'^(?P<pk>\d+)/$', views.BookmarkDetailView, name='detail'),
]