from django.db import router
from django.urls import path, include
from rest_framework import renderers
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

from .views import SnippetViewSet, UserViewSet

schema_view = get_schema_view(title='Pastebin API')


snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, render_classes=[renderers.StaticHTMLRenderer])


user_list = UserViewSet.as_view({
    'get': 'list'
})


user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [path('', include(router.urls)),
               path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
               path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
               path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),
               path('users/', views.UserList.as_view(), name='user-list'),
               path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
               path('schema/', schema_view),
               ]

