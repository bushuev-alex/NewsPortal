from news.models import *
from modeltranslation.translator import register, TranslationOptions  # импортируем декоратор для перевода и класс настроек, от которого будем наследоваться


# регистрируем наши модели для перевода

# @register(Author)
# class CategoryTranslationOptions(TranslationOptions):
#     fields = ('user',)  # указываем, какие именно поля надо переводить в виде кортежа

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # указываем, какие именно поля надо переводить в виде кортежа


@register(Post)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('type', 'title', 'text')


@register(Comment)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('text', )
