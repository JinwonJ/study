from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.login),
    path('login/validate', views.login_validate),
    path('join/', views.join_page)
]
