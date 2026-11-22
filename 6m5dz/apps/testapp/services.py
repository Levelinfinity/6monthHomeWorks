from django.core.cache import cache
from .models import Post
from .serializers import PostSerializer


def get_posts():
    posts = cache.get("posts_list")

    if posts is not None:
        return posts

    posts = PostSerializer(Post.objects.all(), many=True).data
    cache.set("posts_list", posts, timeout=60)

    return posts


def create_post(data):
    serializer = PostSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    post = serializer.save()

    cache.delete("posts_list")

    return post