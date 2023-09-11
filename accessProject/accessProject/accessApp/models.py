# your_app_name/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=50, default='User')

    def __str__(self):
        return self.username


class API(models.Model):
    user = models.ForeignKey('accessApp.CustomUser', on_delete=models.CASCADE, related_name='apis')
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    endpoint = models.CharField(max_length=100)
    description = models.TextField()
    mapped_users = models.ManyToManyField('accessApp.CustomUser', related_name='mapped_apis', blank=True)

    def __str__(self):
        return self.name


class Token(models.Model):
    user = models.OneToOneField('accessApp.CustomUser', on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()