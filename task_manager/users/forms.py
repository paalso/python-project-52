# task_manager/users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username')

        labels = {
            'first_name': _('First name'),
            'last_name':  _('Last name'),
            'username':   _('Username'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Delete all the password field validators
        self.fields['password1'].validators.clear()

        # Update the password field help_text
        self.fields['password1'].help_text = _(
            'Your password must contain at least 3 characters.')
        self.fields['password2'].help_text = _(
            'Enter the same password again for verification.')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and len(password1) < 3:
            raise forms.ValidationError(
                _('Your password is too short. '
                  'Password must be at least 3 characters.'))

        return password2


class CustomUserUpdateForm(CustomUserForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = CustomUser.objects.filter(username=username)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                _('A user with this username already exists.'))
        return username
