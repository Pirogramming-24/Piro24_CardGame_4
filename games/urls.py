from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.main_view, name='main'),
    
    # [과제 요구사항에 맞춘 URL 구조 예시 - 나중에 주석 풀고 쓰세요]
    # [cite_start]path('list/', views.game_list_view, name='game_list'), # 게임 목록
    # [cite_start]path('ranking/', views.ranking_view, name='ranking'),  # 랭킹 페이지
    # [cite_start]path('attack/', views.attack_view, name='attack'),     # 공격하기(게임 생성)
    # 1. 공격하기 페이지 (게임 생성)
    # 127.0.0.1:8000/attack/ 주소로 접속 가능
    path('attack/', views.attack_view, name='game_attack'), 
    # 2. 반격하기 페이지 (게임 ID 필요) [cite: 8]
    # 127.0.0.1:8000/counter/1/ 과 같은 주소로 접속 가능
    path('counter/<int:game_id>/', views.counter_attack, name='game_counter'),
]