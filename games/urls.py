from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # 1. 메인 페이지 (main.html / game_list.html)
    path('', views.main_view, name='main'),
   
    # 로그인, 회원가입 (views.py에 해당 함수가 정의되어 있어야 합니다)
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),

    # 2. 공격하기 (game_attack.html)
    path('attack/', views.attack_view, name='game_attack'),

    # 3. 게임 상세 (game_detail.html)
    path('detail/<int:pk>/', views.game_detail_view, name='game_detail'),

    # 4. 반격하기
    path('counter/<int:game_id>/', views.counter_attack, name='counter_attack'),

    # 5. 랭킹 (ranking.html)
    path('ranking/', views.ranking_list, name='ranking'),

    # [핵심] 게임 상태 확인용 URL (이 부분이 있어야 로딩화면에서 에러가 안 납니다!)
    path('check_status/<int:game_id>/', views.check_game_status, name='check_game_status'),
]