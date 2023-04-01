from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostFilter
from datetime import datetime


class PostList(ListView):
    model = Post  # Указываем модель, объекты которой мы будем выводить
    ordering = '-date_time'  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'news.html'  # Указываем имя шаблона, в котором будут все инструкции о том, # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'  # Это имя списка, в котором будут лежать все объекты. # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_news'] = None
        return context


class SearchNews(ListView):
    model = Post  # Указываем модель, объекты которой мы будем выводить
    ordering = '-date_time'  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'search.html'  # Указываем имя шаблона, в котором будут все инструкции о том, # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'  # Это имя списка, в котором будут лежать все объекты. # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 2

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_news'] = None
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — news.html
    template_name = 'news_by_id.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context