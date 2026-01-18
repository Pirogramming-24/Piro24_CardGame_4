import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Game

def main_view(request):
    return render(request, 'games/main.html') # 일단 파일명 가칭(나중에 수정하셔요)

# 1. 랭킹 페이지 조회 (백엔드 3)
def ranking_list(request):
    User = get_user_model()
    # 누적 점수(points) 기준 내림차순 정렬 
    users = User.objects.all().order_by('-points')
    return render(request, 'ranking.html', {'users': users})

# 2. 반격하기 및 결과 판정 로직 (백엔드 3)
def counter_attack(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # 이미 반격이 완료된 게임이면 결과 페이지로 리다이렉트
    if game.defender_card is not None:
        return redirect('game_detail', game_id=game.id)

    if request.method == 'POST':
        # 프론트에서 전달받은 수비자의 카드 숫자 
        selected_card = int(request.POST.get('selected_card'))
        game.defender_card = selected_card
        
        # [결과 판정 로직 시작]
        # 1. 무승부 판정: 숫자가 같으면 점수 변동 없음 
        if game.attacker_card == selected_card:
            game.winner = None 
        else:
            # 2. 승리 기준 랜덤 결정 (0: 큰 수 승리, 1: 작은 수 승리)
            criterion = random.choice([0, 1])
            # (주의) 모델에 win_criterion 필드를 추가해야 저장 가능합니다.
            game.win_criterion = criterion
            
            att_card = game.attacker_card
            def_card = game.defender_card
            
            # 3. 승자 판정 및 점수 계산 
            is_attacker_win = (criterion == 0 and att_card > def_card) or \
                              (criterion == 1 and att_card < def_card)
            
            if is_attacker_win:
                game.winner = game.attacker
                # 승자는 자기 카드만큼 +, 패자는 자기 카드만큼 
                game.attacker.points += att_card
                game.defender.points -= def_card
            else:
                game.winner = game.defender
                game.defender.points += def_card
                game.attacker.points -= att_card
            
            # 유저별 누적 점수 업데이트 저장
            game.attacker.save()
            game.defender.save()
            
        game.save()
        return redirect('game_detail', game_id=game.id) # 반격 후 상세 페이지로 