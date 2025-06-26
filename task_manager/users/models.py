from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    @property
    def full_name(self):
        fn = f"{self.first_name} {self.last_name}".strip()
        return fn if fn else self.username

    # TODO: Check if it's needed
    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return f'user {self.id} - {self.username}, full name {self.full_name}'
