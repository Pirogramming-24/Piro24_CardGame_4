from django.db import models
from django.conf import settings # 유저 모델을 가져오는 정석 방법

class Game(models.Model):
    # 1. 공격자 (게임을 만든 사람)
    attacker = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='attack_games'
    )
    # 2. 수비자 (공격을 당하는 사람)
    defender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='defend_games'
    )
    
    # 3. 공격자의 카드 (랜덤 5개 중 선택한 1개)
    attacker_card = models.IntegerField()
    
    # 4. 수비자의 카드 (아직 모름 -> null=True)
    defender_card = models.IntegerField(null=True, blank=True)
    
    # 5. 게임 상태 (진행중 / 종료 / 취소 등) 
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='won_games'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    # 6. 승리 기준 (0: 큰 수 승리, 1: 작은 수 승리)
    # 반격 시점에 random으로 결정되어 저장됨
    win_criterion = models.IntegerField(null=True, blank=True)

    # 7. 게임 상태 (선택 사항: '진행중', '종료', '무승부' 등을 구분)
    def __str__(self):
        return f"{self.attacker} vs {self.defender}"
    
