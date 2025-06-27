from django.forms import ModelForm

from .models import CustomUser


class CustomUserCreationForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'password')
