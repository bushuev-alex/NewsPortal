from django.contrib import admin
from django.urls import path, include
from api.views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'authors', AuthorViewset)
router.register(r'comments', CommentViewset)
router.register(r'categories', CategoryViewset)
router.register(r'posts', PostViewset, basename='posts')




urlpatterns = [
   # path('posts/', PostListAPI.as_view(), name='post_api'),
   path(r'', include(router.urls)),
   # path('/posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
   # path('search/', SearchNews.as_view()),
   # path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
   # path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
   #
   # path('news/create/', NewsCreate.as_view(), name='post_create'),
   # # path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
   # path('news/<int:pk>/edit/', NewsUpdate.as_view()),
   # path('news/<int:pk>/delete/', NewsDelete.as_view(), name='delete_news'),
   #
   # path('articles/create/', ArticleCreate.as_view()),
   # # path('articles/<int:pk>/', ArticlesDetail.as_view(), name='articles_detail'),
   # path('articles/<int:pk>/edit/', ArticleUpdate.as_view()),
   # path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='delete_article'),
]
