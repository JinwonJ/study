from django.urls import re_path
from .splitviews import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    re_path(r'^register/$', RegisterAccountsView, name='pn_reg_accounts'),
    re_path(r'^login/$', LoginView, name='pn_login'),
    re_path(r'^logout/$', LogoutView, name='pn_logout'),
    re_path(r'^modify/$', AccountsModifyView, name='pn_accounts_modify'),
    re_path(r'^password_modify/$', PasswordModifyView, name='pn_password_modify'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)