from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (PostApiView, PostLikeView, PostDislikeView, PostsAnalyticsView)

router = DefaultRouter()
router.register(r'', PostApiView, basename='post')

urlpatterns = [
    path('like/<int:id>/', PostLikeView.as_view(), name='like'),
    path('dislike/<int:id>/', PostDislikeView.as_view(), name='dislike'),
    path('analytics/', PostsAnalyticsView.as_view(), name='post_analytics'),
]
urlpatterns += router.urls
