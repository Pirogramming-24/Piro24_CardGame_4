from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # settings를 임포트합니다.

class User(AbstractUser):
    points = models.IntegerField(default=0)
    nickname = models.CharField(max_length=50, blank=True) # 닉네임 필드 추가

    def __str__(self):
        return self.username
    
