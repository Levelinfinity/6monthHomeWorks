from django.shortcuts import render
from .models import Lesson
from .serializers import LessonSerializer
from rest_framework import generics, status
from .permissions import IsTeacherOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import google_auth_service

# Create your views here.

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrReadOnly]


class GoogleAuthView(APIView):
    permission_classes = [] 

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({"error": "Поле 'code' обязательно."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = google_auth_service(code)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )