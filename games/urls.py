from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # 1. 메인 페이지 (main.html / game_list.html)
    path('', views.main_view, name='main'),

    # 2. 공격하기 (game_attack.html)
    path('attack/', views.attack_view, name='game_attack'),

    # 3. 게임 상세 (game_detail.html)
    path('detail/<int:pk>/', views.game_detail_view, name='game_detail'),

    # 4. 반격하기 (game_counter.html)
    path('counter/<int:game_id>/', views.counter_attack, name='game_counter'),

    # 5. 랭킹 (ranking.html)
    path('ranking/', views.ranking_list, name='ranking'),
]