from django.shortcuts import render
from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class CustomUserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "email": user.email,
            "role": getattr(user, 'role', 'client'),
            "is_staff": user.is_staff,
            "date_joined": user.date_joined,
        }
        return Response(data, status=status.HTTP_200_OK)