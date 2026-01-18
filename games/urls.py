from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.main_view, name='main'),
    
    # [과제 요구사항에 맞춘 URL 구조 예시 - 나중에 주석 풀고 쓰세요]
    # [cite_start]
    #path('list/', views.game_list_view, name='game_list'), # 게임 목록
    # [cite_start]
    #path('ranking/', views.ranking_view, name='ranking'),  # 랭킹 페이지
    # [cite_start]
    #path('attack/', views.attack_view, name='game_attack'),     # 공격하기(게임 생성)
    # path('ranking/', views.ranking_list, name='ranking'), # 랭킹 페이지 주소 설정 [cite: 80]
    # 반격하기 처리 주소 (게임 ID를 넘겨받아야 함)
    # path('counter/<int:game_id>/', views.counter_attack, name='counter_attack'),
]