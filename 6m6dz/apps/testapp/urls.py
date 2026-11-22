from django.urls import path
from apps.testapp.views import RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
]