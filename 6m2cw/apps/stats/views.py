from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import get_stats

# Create your views here.

class StatsView(APIView):
    def get(self, request):
        return Response(get_stats())