from django.contrib import admin
from .models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'author', 'price', 'url')

admin.site.register(Book, BookAdmin)