from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # 1. 메인 페이지 (비로그인 대문)
    path('', views.main_view, name='main'),
    
    # [로그인 후] Start 버튼 화면
    path('home/', views.main_logined_view, name='main_logined'),

    # 2. 게임 기능
    path('attack/', views.attack_view, name='game_attack'),
    path('counter/<int:game_id>/', views.counter_attack, name='counter_attack'),
    path('detail/<int:pk>/', views.game_detail_view, name='game_detail'),
    path('ranking/', views.ranking_list, name='ranking'),
    
    # [핵심] 전적 리스트 경로 (이게 빠져서 에러가 난 것입니다!)
    path('list/', views.game_list, name='game_list'),
    
    # 3. 기타 기능 (취소, 상태확인)
    path('cancel/<int:game_id>/', views.cancel_duel, name='cancel_duel'),
    path('check_status/<int:game_id>/', views.check_game_status, name='check_game_status'),
]