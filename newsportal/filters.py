from django_filters import FilterSet, DateTimeFilter
from django.forms import DateTimeInput
from .models import *

class PostFilter(FilterSet):
   added_after = DateTimeFilter(
        field_name='time_created',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
   class Meta:
    model = Post
    fields = {
           'category':['exact'],
           'title': ['icontains'],
    }