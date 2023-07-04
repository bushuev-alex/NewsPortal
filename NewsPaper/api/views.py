from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


from news.serializers import *
from news.models import *


class PostListAPI(APIView):

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer_context = {'request': request}
        serializer = PostSerializer(posts, context=serializer_context, many=True)
        return Response(serializer.data)


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
