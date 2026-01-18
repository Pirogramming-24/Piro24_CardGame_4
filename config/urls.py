from django.contrib import admin
from django.urls import path, include  # [중요] include를 꼭 가져와야 합니다!

urlpatterns = [
    path('admin/', admin.site.urls),

    #소셜 로그인 (allauth)
    # 'accounts/'로 시작하는 주소는 다 allauth가 처리하게 맡김 (예: accounts/login/, accounts/google/login/)
    path('accounts/', include('allauth.urls')),

    # 게임 관련 기능 (games 앱)
    # 위 두 개가 아닌 나머지 주소는 다 games 폴더의 urls.py로 보냄
    path('', include('games.urls')),
]