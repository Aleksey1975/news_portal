from django import forms
from django.core.exceptions import ValidationError

from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'content',
          ]

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("title")
        if description is not None and len(description) < 2:
            raise ValidationError({
                "title": "Название не может быть менее 2 символов."
            })
        description = cleaned_data.get("content")
        if description is not None and len(description) < 10:
            raise ValidationError({
                "title": "Содержание не может быть менее 10 символов."
            })

        return cleaned_data


