from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # settings를 임포트합니다.

class User(AbstractUser):
    points = models.IntegerField(default=0)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.username
    
