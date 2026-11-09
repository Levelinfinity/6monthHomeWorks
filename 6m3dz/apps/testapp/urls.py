from django.urls import path
from .views import CustomUserListCreateView, CustomUserRetrieveUpdateDestroyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import LogoutView, ProfileStatsView

urlpatterns = [
    path('users/', CustomUserListCreateView.as_view(), name='customuser-list-create'),    
    path('users/<int:pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name='customuser-detail'),
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('logout/', LogoutView.as_view(), name='logout'),                     
    path('profile/stats/', ProfileStatsView.as_view(), name='profile-stats'), 
]