from typing import Any, Mapping, Optional, Type, Union
from django import forms
from django.forms.utils import ErrorList
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AddArticleForm(forms.ModelForm):
    category = forms.MultipleChoiceField(
        widget=forms.Select(attrs={'class': 'autocomplete', 'data-autocomplete-url': '/autocomplete/', 'type': 'hidden', 'id': 'select_cat'}),
        choices=[],
        required=False,
    )

    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'category']
        widgets = {
            'title': forms.TextInput(),
            'content': forms.Textarea(),
            'category': forms.TextInput(),
        }

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Comment'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddCommentForm, self).__init__(*args, **kwargs)

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Search', 'id': 'input', 'list': 'res'}))