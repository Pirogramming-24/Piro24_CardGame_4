from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 커스텀 유저 모델을 관리자 페이지에 등록
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 상세 페이지에서 보일 필드 구성
    fieldsets = UserAdmin.fieldsets + (
        ('추가 정보', {
            'fields': ('points', 'nickname'),
        }),
    )

    # 유저 생성 페이지에서도 보이게 하고 싶으면
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('추가 정보', {
            'fields': ('points', 'nickname'),
        }),
    )

    # 리스트 화면에서 보고 싶으면
    list_display = ('username', 'nickname', 'points', 'is_staff')