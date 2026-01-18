from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.main_view, name='main'),
    
    # [과제 요구사항에 맞춘 URL 구조 예시 - 나중에 주석 풀고 쓰세요]
    # [cite_start]path('list/', views.game_list_view, name='game_list'), # 게임 목록
    # [cite_start]path('ranking/', views.ranking_view, name='ranking'),  # 랭킹 페이지
    # [cite_start]path('attack/', views.attack_view, name='attack'),     # 공격하기(게임 생성)
]