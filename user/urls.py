from django.urls import path

from .views import UserActivityDetailView

urlpatterns = [
    path('activity/<int:id>/', UserActivityDetailView.as_view(), name='user_activity')
]
