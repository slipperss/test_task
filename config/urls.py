from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import settings
from post.views import CommentView
from user.views import CustomTokenObtainPairView
from .yasg import urlpatterns as doc_urls

router = DefaultRouter()
router.register(r'comment', CommentView, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path('auth/', include('djoser.urls.jwt')),
    path('api/post/', include('post.urls')),
    path('api/user/', include('user.urls')),
    path('api/', include(router.urls))
]
urlpatterns += doc_urls
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
