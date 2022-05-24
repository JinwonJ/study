from typing import Pattern
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import RedirectView
from django_pydenticon.views import image as pydenticon_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('identicon/image/<path:data>/',pydenticon_image,name='pydenticon_image'),
    path('instagram/', include('instagram.urls')),
    path('', login_required(RedirectView.as_view(pattern_name='instagram:Index')),name='root'),
]

if settings.DEBUG :  #미디어 파일에 대한 스태틱 서브 기능
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)