from django import forms
from .models import Author
from django.contrib.auth.models import User


class AddAuthorForm(forms.Form):
    username = forms.CharField(max_length=80)
    password = forms.CharField(widget=forms.PasswordInput)
    bio = forms.CharField(widget=forms.Textarea)
    # user = forms.ModelChoiceField(queryset=User.objects.all())


class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=100)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(widget=forms.Textarea)
    time_required = forms.CharField(max_length=30)
    instructions = forms.CharField(widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
