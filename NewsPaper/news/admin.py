from django.contrib import admin
from news.models import Post, Category, PostCategory, Author, Comment
from modeltranslation.admin import TranslationAdmin


# class AuthorAdmin(TranslationAdmin):
#     model = Author


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostModelAdmin(TranslationAdmin):
    model = Post


class CommentModelAdmin(TranslationAdmin):
    model = Comment


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Author)
admin.site.register(Comment)



