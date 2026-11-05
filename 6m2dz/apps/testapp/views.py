from django.shortcuts import render
from rest_framework.views import APIView
from .permissions import IsAdminOnly, IsUserOnly
from rest_framework.response import Response

# Create your views here.

class AdminPanelAPIView(APIView):
    permission_classes = [IsAdminOnly]

    def get(self, request):
        return Response({'message': 'Добро пожаловать в панель администратора!'})


class UserPanelAPIView(APIView):
    permission_classes = [IsUserOnly]

    def get(self, request):
        return Response({'message': 'Добро пожаловать в личный кабинет пользователя!'})