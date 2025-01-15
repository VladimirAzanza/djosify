from django.contrib.auth.models import AbstractUser, AbstractBaseUser
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
