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
    
    # 5. 게임 상태 (진행중 / 종료 / 취소 등) - 최명규님 파트와 연결됨
    # 승패 결과는 최명규님이 하겠지만, 데이터 저장 공간은 여기서 만들어둬야 함
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='won_games'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attacker} vs {self.defender}"