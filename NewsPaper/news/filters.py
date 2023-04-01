from django_filters import FilterSet, NumberFilter, CharFilter, DateTimeFilter
from django_filters.widgets import RangeWidget
from .models import Post


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):

    date_time__lt = DateTimeFilter(field_name='date_time', lookup_expr='lt')

    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'title': ['icontains'],
            # 'category': ['icontains'],
            'rating': ['lt', 'gt']
            # 'date_time'
        }
