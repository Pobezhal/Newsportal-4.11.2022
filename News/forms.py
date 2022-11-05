

from django import forms
from django.core.exceptions import ValidationError
from .models import *

class PostForm(forms.ModelForm):
    content = forms.CharField(min_length=20)
    class Meta:
       model = Post
       fields =  [
           'author',
           'title',
           'post_type',
           'content',
           'category',
       ]



    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        title = cleaned_data.get("title")

        if title == content:
            raise ValidationError({
                "Название!": "Текст публикации не должен быть идентичен названию."
            })
        return cleaned_data
