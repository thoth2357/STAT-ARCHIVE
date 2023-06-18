from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
