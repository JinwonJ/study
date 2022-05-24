from django.urls import re_path
from .splitviews import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'pystagram'

urlpatterns = [
    re_path(r'^$', MainView, name='pn_main'),
    re_path(r'^(?P<user_id>[a-zA-Z0-9-_.]*)/$', PostListView, name='pn_post_list'),
    re_path(r'^p/(?P<post_id>[0-9]+)/$', PostDetailView, name='pn_post_detail'),
    re_path(r'^p/upload/$', PostUploadView, name='pn_post_upload'),
    re_path(r'^p/modify/(?P<post_id>[0-9]+)/$', PostModifyView, name='pn_post_modify'),
    re_path(r'^p/delete/(?P<post_id>[0-9]+)/$', PostDeleteView, name='pn_post_delete'),
    re_path(r'^follow/(?P<following_id>[a-zA-Z0-9-_.]*)/$', FollowView, name='pn_follow'),
    re_path(r'^unfollow/(?P<following_id>[a-zA-Z0-9-_.]*)/$', UnfollowView, name='pn_unfollow'),
    re_path(r'^like/(?P<post_id>[0-9]+)/$', LikePostView, name='pn_like_post'),
    re_path(r'^unlike/(?P<post_id>[0-9]+)/$', UnlikePostView, name='pn_unlike_post'),
    re_path(r'^bookmark/(?P<post_id>[0-9]+)/$', BookmarkView, name='pn_bookmark'),
    re_path(r'^unbookmark/(?P<post_id>[0-9]+)/$', UnbookmarkView, name='pn_unbookmark'),
    re_path(r'^p/search/$', SearchView, name='pn_search'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)