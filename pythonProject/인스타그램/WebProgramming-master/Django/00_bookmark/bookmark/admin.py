from django.contrib import admin
# models.py에서 만든 Bookmark 클래스를 import
from bookmark.models import Bookmark

# Register your models here.
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')

# models.py에서 만든 Bookmark 클래스와 BookmarkAdmin 클래스를 연결시켜
# list_display의 id, name, url을 Bookmark 클래스에서 가져오도록 함
admin.site.register(Bookmark, BookmarkAdmin)