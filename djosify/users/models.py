import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField('Email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def __str__(self):
        self.email


User = get_user_model()


class UserRefreshToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    refresh_token = models.CharField(
        max_length=512, unique=True, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Tokens for {self.user.email}'
