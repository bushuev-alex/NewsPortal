from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponse
from django.views import View
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.conf import settings

from datetime import datetime
import pytz

from rest_framework import viewsets
from rest_framework import permissions

from news.filters import PostFilter
from news.forms import *
from news.utils import too_many_posts, msg
from news.signals import notify_about_new_creation, printer2
from news.tasks import printer
from news.serializers import *
from news.models import *


# LIST OF NEWS
class PostList(ListView):
    model = Post  # Указываем модель, объекты которой мы будем выводить
    ordering = '-date_time'  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'news.html'  # Указываем имя шаблона, в котором будут все инструкции о том, # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'news'  # Это имя списка, в котором будут лежать все объекты. # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 10

    def get_context_data(self, **kwargs):
        printer.delay()
        printer2.delay()
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.now()
        # context['hour_now'] = context['time_now'].hour
        context['timezones'] = pytz.common_timezones
        context['next_news'] = None
        return context

    def post(self, request, *args, **kwargs):
        # context = self.get_contex_data(**kwargs)
        # context['timezone'] = request.POST['timezone']
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/posts/')


# SEARCH
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
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.now()
        context['next_news'] = None
        # context['next_news_msg'] = gettext("Next news will be soon!")
        # context['models'] = self.model.objects.all()
        context['filterset'] = self.filterset
        return context


# CREATE
class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = "news_edit.html"

    def form_valid(self, form):
        post = form.save(commit=True)
        post.type = "NEWS"

        if too_many_posts(model=self.model, post=post):
            return HttpResponse(msg)
        else:
            notify_about_new_creation.delay(post.pk)
            return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = "news_edit.html"

    def form_valid(self, form):
        post = form.save(commit=True)
        post.type = "POST"

        if too_many_posts(model=self.model, post=post):
            return HttpResponse(msg)
        else:
            notify_about_new_creation.delay(post.pk)
            return super().form_valid(form)


# UPDATE
class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.view_post', 'news.change_post')
    form_class = PostForm
    model = Post
    template_name = "news_edit.html"

    def form_valid(self, form):
        post = form.save(commit=True)
        if post.type == "POST":
            return HttpResponse(gettext("You try to update 'POST' but this one is 'NEWS'"))
        post.type = "NEWS"
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.view_post', 'news.change_post')
    form_class = PostForm
    model = Post
    template_name = "news_edit.html"

    def form_valid(self, form):
        post = form.save(commit=True)
        if post.type == "NEWS":
            return HttpResponse(gettext("You try to update 'NEWS' but this one is 'POST'"))
        post.type = "POST"
        return super().form_valid(form)


# DELETE
@method_decorator(login_required, name='dispatch')
class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.view_post', 'news.delete_post')
    model = Post
    template_name = "news_delete.html"
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        obj = self.get_object()
        if obj.type == "POST":
            return HttpResponse(gettext("You try to delete 'POST' but this one is 'NEWS'"))
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.view_post', 'news.delete_post')
    model = Post
    template_name = "news_delete.html"
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        obj = self.get_object()
        if obj.type == "NEWS":
            return HttpResponse(gettext("You try to delete 'NEWS' but this one is 'POST'"))
        return super().form_valid(form)


# DETAILS
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


class CategoryListView(PostList):
    model = Post
    template_name = 'news_by_cat.html'
    context_object_name = 'news_by_cat'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)  # .group_by("-date_time")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribed'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = gettext("You successfully subscribed on news at category")
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class AuthorViewset(viewsets.ModelViewSet):
   queryset = Author.objects.all()
   serializer_class = AuthorSerializer


class CategoryViewest(viewsets.ModelViewSet):
   queryset = Category.objects.all()
   serializer_class = CategorySerializer


class PostViewset(viewsets.ModelViewSet):
   queryset = Post.objects.all()
   serializer_class = PostSerializer


class CommentViewest(viewsets.ModelViewSet):
   queryset = Comment.objects.all()
   serializer_class = CommentSerializer