import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required # [추가] 로그인 체크용
from .models import Game

# 1. 랜덤 카드 생성 함수 
def get_random_cards():
    cards = random.sample(range(1, 11), 5)
    return sorted(cards)

# 2. 메인 페이지 (로그인 여부에 따라 분기)
def main_view(request):
    if request.user.is_authenticated:
        # 로그인 한 유저 -> 게임 전적 리스트 (나와 관련된 게임만)
        games = Game.objects.filter(attacker=request.user) | Game.objects.filter(defender=request.user)
        # 최신순 정렬 (선택사항)
        games = games.order_by('-created_at')
        return render(request, 'games/game_list.html', {'games': games})
    else:
        # 로그인 안 한 유저 -> 시작 화면
        return render(request, 'games/main_home.html')

# 3. 공격하기 (게임 생성)
@login_required
def attack_view(request):
    User = get_user_model()
    if request.method == 'GET':
        # 카드 5장 뽑기
        cards = get_random_cards()
        # 공격할 상대 찾기 (나 자신은 제외)
        users = User.objects.exclude(id=request.user.id)
        
        context = {
            'cards': cards,
            'users': users
        }
        return render(request, 'games/attack.html', context)
    
    elif request.method == 'POST':
        defender_id = request.POST.get('defender_id')
        card_picked = request.POST.get('card_picked') # 내가 고른 카드

        defender = get_object_or_404(User, id=defender_id)

        # 게임 생성 (DB 저장)
        Game.objects.create(
            attacker=request.user,
            defender=defender,
            attacker_card=int(card_picked),
            defender_card=None,   # 아직 안 고름
            win_criterion=None,   # 반격할 때 정해짐
            winner=None,           # 아직 승자 없음
            result='진행중'        # [중요] 초기 상태 설정
        )

        return redirect('games:main')


# 4. 랭킹 페이지 조회
def ranking_list(request):
    User = get_user_model()
    # 누적 점수(points) 기준 내림차순 정렬 
    users = User.objects.all().order_by('-points')
    return render(request, 'ranking.html', {'users': users})

# 5. 반격하기 및 결과 판정 로직
def counter_attack(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # 이미 반격이 완료된 게임이면 결과 페이지로 리다이렉트
    if game.defender_card is not None:
        # urls.py에 game_detail이 정의되어 있어야 함
        return redirect('games:game_detail', pk=game.id) 

    if request.method == 'POST':
        # 프론트에서 전달받은 수비자의 카드 숫자 
        selected_card = int(request.POST.get('selected_card'))
        game.defender_card = selected_card
        
        # [결과 판정 로직 시작]
        # 1. 무승부 판정: 숫자가 같으면 점수 변동 없음
        if game.attacker_card == selected_card:
            game.winner = None 
            game.result = '무승부' # [추가] 상태 업데이트
        else:
            # 2. 승리 기준 랜덤 결정 (0: 큰 수 승리, 1: 작은 수 승리)
            criterion = random.choice([0, 1])
            game.win_criterion = criterion
            
            att_card = game.attacker_card
            def_card = game.defender_card
            
            # 3. 승자 판정 및 점수 계산
            is_attacker_win = (criterion == 0 and att_card > def_card) or \
                              (criterion == 1 and att_card < def_card)
            
            if is_attacker_win:
                game.winner = game.attacker
                game.result = '승리' # (공격자 기준 승리 표시)
                # 승자는 자기 카드만큼 +, 패자는 자기 카드만큼 -
                game.attacker.points += att_card
                game.defender.points -= def_card
            else:
                game.winner = game.defender
                game.result = '패배'
                game.defender.points += def_card
                game.attacker.points -= att_card
            
            # 유저별 누적 점수 업데이트 저장
            game.attacker.save()
            game.defender.save()
            
        game.save()
        # namespace를 쓴다면 games:game_detail 로 수정 필요할 수 있음
        return redirect('games:game_detail', pk=game.id)