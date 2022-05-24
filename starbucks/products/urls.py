from django.urls import path
from .views import MenuView, CategoryView, ProductView, ProductDetailView

urlpatterns = [
    path('menu', MenuView.as_view()),
    path('/category', CategoryView.as_view()),
    path('/product', ProductView.as_view()),
    path('/product/<int:product_id>', ProductView.as_view()),
    path('/product/<int:product_id>', ProductDetailView.as_view()),
]