from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    @property
    def full_name(self):
        fn = f'{self.first_name} {self.last_name}'.strip()
        return fn if fn else self.username

    def __str__(self):
        return f'user {self.id} - {self.username}, full name {self.full_name}'
