from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'executor', 'labels')

        labels = {
            'name': _('Name'),
            'description':  _('Description'),
            'status':   _('Status'),
            'executor':   _('Executor'),
            'labels':   _('Labels'),
        }
