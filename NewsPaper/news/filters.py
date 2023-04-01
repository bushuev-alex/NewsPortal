from django_filters import FilterSet, NumberFilter, CharFilter, DateTimeFilter, DateFilter
from django.forms import DateInput
from django_filters.widgets import RangeWidget
from .models import Post


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):

    date_time__gt = DateFilter(field_name='date_time', lookup_expr='gt', label='Start Date',
                               widget=DateInput(attrs={'type': 'date'}),
                               )

    date_time__lt = DateFilter(field_name='date_time', lookup_expr='lt', label='End Date',
                               widget=DateInput(attrs={'type': 'date'}),
                               )

    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'title': ['icontains'],
            # 'category': ['icontains'],
            'rating': ['lt', 'gt']
            # 'date_time'
        }
