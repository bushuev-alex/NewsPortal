from django.contrib import admin
from django.urls import path, include
from news.views import PostList, PostDetail, SearchNews, NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleUpdate, ArticleDelete, CategoryListView, subscribe
from news.views import AuthorViewset, CommentViewest, CategoryViewest, PostViewset
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'schools', AuthorViewset)
router.register(r'classes', CommentViewest)
router.register(r'students', CategoryViewest)
router.register(r'students', PostViewset)


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('search/', SearchNews.as_view()),
   path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),

   path('news/create/', NewsCreate.as_view(), name='post_create'),
   # path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view()),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='delete_news'),

   path('articles/create/', ArticleCreate.as_view()),
   # path('articles/<int:pk>/', ArticlesDetail.as_view(), name='articles_detail'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view()),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='delete_article'),

   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
