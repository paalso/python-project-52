# task_manager/users/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = 'name',

        labels = {
            'name': _('Name'),
        }
