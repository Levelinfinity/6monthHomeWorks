from django.urls import path
from .views import LessonListCreateView, GoogleAuthView

urlpatterns = [
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('auth/google/', GoogleAuthView.as_view(), name='google-auth'),
]