import django_filters
from django.forms import DateInput
from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import *


class PostFilter(FilterSet):
   post_time = DateFilter(lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))
   categoria = ModelChoiceFilter(
       field_name = 'category',
       queryset = Category.objects.all(),
       label = 'Категория',
       empty_label = 'Любая',)

   Avtor = ModelChoiceFilter(
        field_name = 'author_id',
        queryset = Author.objects.all(),
        label = 'Автор',
        empty_label = 'Все писаки',)



   class Meta:

       model = Post
       fields = {
           # поиск по названию
           'title': ['icontains'],

      }


