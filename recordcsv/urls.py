from django.urls import path
from .views import UploadPageView, UserListView, UploadView

urlpatterns = [
    path('upload/', UploadPageView.as_view(), name='upload_page'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('api/upload/', UploadView.as_view(), name='api_upload')
]