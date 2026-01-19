from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # 1. 메인 페이지 (비로그인 대문)
    path('', views.main_view, name='main'),
    
    # [핵심 추가] 로그인 후 Start 화면 경로 (이게 없어서 에러가 난 겁니다!)
    path('home/', views.main_logined_view, name='main_logined'),

    # 2. 게임 기능
    path('attack/', views.attack_view, name='game_attack'),
    path('counter/<int:game_id>/', views.counter_attack, name='counter_attack'),
    path('detail/<int:pk>/', views.game_detail_view, name='game_detail'),
    path('ranking/', views.ranking_list, name='ranking'),
    
    # 3. 기타 기능 (취소, 상태확인)
    path('cancel/<int:game_id>/', views.cancel_duel, name='cancel_duel'),
    path('check_status/<int:game_id>/', views.check_game_status, name='check_game_status'),
]