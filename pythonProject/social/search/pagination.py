from rest_framework.pagination import CursorPagination

class SerchPagination(CursorPagination):

    ordering = "-created_at"
    page_size = 10

