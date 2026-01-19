# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta): # 기본 Meta 상속
        model = User
        # 'first_name' 대신 'nickname'을 포함시킵니다.
        fields = UserCreationForm.Meta.fields + ('nickname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # HTML 템플릿에서 'Name'으로 표시되는 필드의 라벨 변경
        self.fields['nickname'].label = "Name"