# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# 현재 활성화된 유저 모델을 가져옵니다 (users.User)
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # <--- 중요! 우리가 만든 유저 모델과 연결
        # 폼에 표시할 필드들 (비밀번호는 알아서 포함됨)
        # HTML에서 name="first_name"으로 보낸 닉네임도 여기서 받아줍니다.
        fields = ('username', 'first_name')