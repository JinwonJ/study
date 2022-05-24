from django.contrib import admin
from django.urls import path
from authentication.views import registration_view # 추가

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', registration_view, name='register_user'), # 추가

]