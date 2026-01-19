from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # 1. 메인 페이지 (로그인 여부에 따라 '대문' 또는 '게임리스트'를 보여줍니다)
    path('', views.main_view, name='main'),
    
    # 2. 유저 관련 (로그인, 회원가입)
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),

    # 3. 게임 기능 (공격, 반격, 결과, 랭킹)
    path('attack/', views.attack_view, name='game_attack'),
    path('counter/<int:game_id>/', views.counter_attack, name='counter_attack'),
    path('detail/<int:pk>/', views.game_detail_view, name='game_detail'),
    path('ranking/', views.ranking_list, name='ranking'),
    
    # 4. API (상태 확인용)
    path('check_status/<int:game_id>/', views.check_game_status, name='check_game_status'),
    path('cancel/<int:game_id>/', views.cancel_duel, name='cancel_duel'),
]