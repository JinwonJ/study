from rest_framework.pagination import PageNumberPagination

class SaallSetPagination(PageNumberPagination):
    page_size = 3