from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostSerializer
from .services import get_posts, create_post

# Create your views here.

class PostListView(APIView):

    def get(self, request):
        posts = get_posts()
        return Response(posts)

    def post(self, request):
        post = create_post(request.data)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)