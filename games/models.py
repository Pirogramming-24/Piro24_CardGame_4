# games/models.py
from django.db import models
from django.conf import settings

class Game(models.Model):
    # 1. 승리 기준 정의 (가독성을 위해 상수화)
    WIN_LARGE = 0
    WIN_SMALL = 1
    WIN_CRITERION_CHOICES = [
        (WIN_LARGE, '큰 수 승리'),
        (WIN_SMALL, '작은 수 승리'),
    ]

    # 2. 게임 상태 정의
    STATUS_PROGRESS = '진행중'
    STATUS_FINISHED = '종료'
    STATUS_DRAW = '무승부'

    # 3. 유저 관계 설정 (공격자, 수비자, 승리자)
    attacker = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='attack_games',
        verbose_name="공격자"
    )
    defender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='defend_games',
        verbose_name="수비자"
    )
    winner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # 유저가 탈퇴해도 게임 기록은 유지
        null=True, 
        blank=True,
        related_name='won_games',
        verbose_name="승리자"
    )

    # 4. 카드 정보 (공격 시 카드와 수비 시 카드)
    attacker_card = models.IntegerField(verbose_name="공격자 카드")
    defender_card = models.IntegerField(null=True, blank=True, verbose_name="수비자 카드")

    # 5. 게임 결과 및 기준
    result = models.CharField(
        max_length=10, 
        default=STATUS_PROGRESS,
        verbose_name="게임 결과"
    )
    win_criterion = models.IntegerField(
        choices=WIN_CRITERION_CHOICES, 
        null=True, 
        blank=True,
        verbose_name="승리 기준"
    )

    # 6. 시간 정보
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="최종 수정 시간")

    class Meta:
        ordering = ['-created_at'] # 최신 게임이 위로 오도록 정렬

    def __str__(self):
        return f"[{self.id}] {self.attacker.nickname} vs {self.defender.nickname} ({self.result})"