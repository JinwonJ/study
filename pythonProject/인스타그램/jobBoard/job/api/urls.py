from django.urls import path
from job.api.views import JobOfferListAPIView, JobOfferDetailAPIView

urlpatterns = [
    path('jobs/', JobOfferListAPIView.as_view(),
         name='jobs-list'),

    path('jobs/<int:pk>/', JobOfferDetailAPIView.as_view(),
         name='jobs-detail'),
]