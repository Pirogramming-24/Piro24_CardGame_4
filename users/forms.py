# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # signup.html에 있는 필드들을 추가해줍니다.
        fields = UserCreationForm.Meta.fields + ('points',)