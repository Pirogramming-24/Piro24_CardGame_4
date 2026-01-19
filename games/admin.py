from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    # 관리자 목록에서 보여줄 컬럼들
    list_display = ('attacker', 'defender', 'attacker_card', 'defender_card', 'result', 'winner')
    # 클릭해서 들어갈 수 있는 링크 설정
    list_display_links = ('attacker', 'defender')