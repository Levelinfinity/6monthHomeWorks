from django.urls import path
from .views import AdminPanelAPIView, UserPanelAPIView

urlpatterns = [
    path('admin-panel/', AdminPanelAPIView.as_view(), name='admin-panel'),
    path('user-panel/', UserPanelAPIView.as_view(), name='user-panel'),
]