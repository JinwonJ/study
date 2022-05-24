from django.urls import re_path
from .views import *

app_name = 'dkea'

urlpatterns = [
    re_path(r'^$', MainView, name='main'),
    re_path(r'^list/(?P<c_code>c\d+)/$', ProductListView, name='list'),
    re_path(r'^detail/(?P<p_id>\d+)/$', ProductDetailView, name='detail'),
]