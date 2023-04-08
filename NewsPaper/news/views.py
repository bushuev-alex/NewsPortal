from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from datetime import datetime
from .forms import *
from django.urls import reverse, reverse_lazy
from django.http import Http404


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
        context['time_now'] = datetime.utcnow()
        context['next_news'] = None
        return context


class SearchNews(ListView):
    model = Post  # Указываем модель, объекты которой мы будем выводить
    ordering = '-date_time'  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'search.html'  # Указываем имя шаблона, в котором будут все инструкции о том, # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'  # Это имя списка, в котором будут лежать все объекты. # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 10

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


# Create

class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = "news_edit.html"

    def form_valid(self, form):
        post = form.save(commit=True)
        post.type = "NEWS"
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = "news_edit.html"

    def form_valid(self, form):
        post = form.save(commit=True)
        post.type = "POST"
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = "news_edit.html"

    def form_valid(self, form):
        post = form.save(commit=True)
        if post.type == "POST":
            raise Http404("You try to update 'POST' but this one is 'NEWS'")
        post.type = "NEWS"
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = "news_edit.html"

    def form_valid(self, form):
        post = form.save(commit=True)
        if post.type == "NEWS":
            raise Http404("You try to update 'NEWS' but this one is 'POST'")
        post.type = "POST"
        return super().form_valid(form)


# Delete

class NewsDelete(DeleteView):
    model = Post
    template_name = "news_delete.html"
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        obj = self.get_object()
        if obj.type == "POST":
            raise Http404("You try to delete 'POST' but this one is 'NEWS'")
        return super().form_valid(form)


class ArticleDelete(DeleteView):
    model = Post
    template_name = "news_delete.html"
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        obj = self.get_object()
        if obj.type == "NEWS":
            raise Http404("You try to delete 'NEWS' but this one is 'POST'")
        return super().form_valid(form)


# Details

class PostDetail(DetailView):
    model = Post
    template_name = 'news_by_id.html'
    context_object_name = 'news'


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_by_id.html'
    context_object_name = 'news'


class ArticlesDetail(DetailView):
    model = Post
    template_name = 'news_by_id.html'
    context_object_name = 'news'
