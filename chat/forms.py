from django import forms

from .models import *

class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)