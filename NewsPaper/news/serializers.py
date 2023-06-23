from news.models import *
from rest_framework import serializers


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Author
       fields = ['user', 'rating', ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Category
       fields = ['name', 'subscribers', ]


class PostSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Post
       fields = ['author', 'type', 'date_time', 'category', 'title', 'text', 'rating']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Comment
       fields = ['post', 'user', 'text', 'date_time', 'rating']
