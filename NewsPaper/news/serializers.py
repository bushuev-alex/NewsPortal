from news.models import *
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['user', 'rating', ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', ]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['author', 'category', 'type', 'date_time', 'title', 'text', 'rating']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'user', 'text', 'rating']
