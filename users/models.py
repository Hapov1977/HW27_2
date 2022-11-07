
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):

    ROLES = [
        ('admin', "Админ"),
        ('moderator', "Модератор"),
        ('member', "Просто пользователь"),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='member')
    age = models.SmallIntegerField(null=True)
    location = models.ForeignKey('ads.LocationModel', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"