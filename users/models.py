from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    points = models.IntegerField(default=0)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.username