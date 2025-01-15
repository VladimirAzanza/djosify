from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    def __str__(self):
        self.username
