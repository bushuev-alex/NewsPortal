from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, SearchNews, NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleUpdate, ArticleDelete


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('search/', SearchNews.as_view()),

   path('news/create/', NewsCreate.as_view()),
   # path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view()),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='delete_news'),

   path('articles/create/', ArticleCreate.as_view()),
   # path('articles/<int:pk>/', ArticlesDetail.as_view(), name='articles_detail'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view()),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='delete_article'),
]
