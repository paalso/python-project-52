from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'), widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'form-control',
    }))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control',
    }))
