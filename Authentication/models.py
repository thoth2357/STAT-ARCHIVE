from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_email_verified = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_expiration = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username
