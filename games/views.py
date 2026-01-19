import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from django.db.models import Q
from .models import Game

# 1. 유틸리티 함수
def get_random_cards():
    """1부터 10까지의 숫자 중 랜덤으로 5개를 뽑아 정렬하여 반환"""
    cards = random.sample(range(1, 11), 5)
    return sorted(cards)

# 2. 뷰 함수

# [메인 페이지] : 비로그인 유저용 대문
def main_view(request):
    if request.user.is_authenticated:
        return redirect('games:main_logined')
    return render(request, 'games/main.html')

# [로그인 후 메인] : Start 버튼 있는 화면 (이 함수가 꼭 있어야 합니다!)
@login_required
def main_logined_view(request):
    return render(request, 'games/main_logined.html')

# [공격하기] : 게임 생성 및 대결 요청 모달 확인
@login_required
def attack_view(request):
    User = get_user_model()
    
    if request.method == 'GET':
        random_cards = get_random_cards()
        other_users = User.objects.exclude(id=request.user.id)
        
        # [모달용] 나에게 온 대결 요청 확인
        pending_game = Game.objects.filter(defender=request.user, result='진행중').first()
        
        context = {
            'random_cards': random_cards, 
            'other_users': other_users,
            'pending_game': pending_game
        }
        return render(request, 'games/game_attack.html', context)
    
    elif request.method == 'POST':
        defender_id = request.POST.get('defender') 
        card_picked = request.POST.get('selected_card') 

        if not defender_id or not card_picked:
             return redirect('games:game_attack')

        try:
            defender = User.objects.get(id=defender_id)
            
            game = Game.objects.create(
                attacker=request.user,
                defender=defender,
                attacker_card=int(card_picked),
                result='진행중'
            )
            
            # 공격 성공 시 상세 페이지로 이동
            return redirect('games:game_detail', pk=game.id)
            
        except User.DoesNotExist:
            return redirect('games:game_attack')

# [반격하기] : 결과 판정 및 점수 계산
@login_required
def counter_attack(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # 이미 방어한 게임이면 결과 페이지로 이동
    if game.defender_card is not None:
        return redirect('games:game_detail', pk=game.id)

    # [GET] 반격 페이지 렌더링
    if request.method == 'GET':
        random_cards = get_random_cards()
        context = {
            'game': game,
            'random_cards': random_cards
        }
        return render(request, 'games/game_counter.html', context)

    # [POST] 카드 선택 및 결과 처리
    elif request.method == 'POST':
        selected_card = request.POST.get('selected_card')
        
        if not selected_card:
            return redirect('games:counter_attack', game_id=game.id)

        selected_card = int(selected_card)
        game.defender_card = selected_card
        
        # --- 승패 판정 로직 ---
        if game.attacker_card == selected_card:
            game.winner = None 
            game.result = '무승부'
        else:
            # 0: 큰 수 승리, 1: 작은 수 승리
            criterion = random.choice([0, 1])
            game.win_criterion = criterion
            
            att = game.attacker_card
            def_c = game.defender_card
            
            # 승리 조건 판단
            if criterion == 0:
                is_attacker_win = att > def_c
            else:
                is_attacker_win = att < def_c
            
            if is_attacker_win:
                game.winner = game.attacker
                game.result = '승리'
                game.attacker.points += att
                game.defender.points -= def_c
            else:
                game.winner = game.defender
                game.result = '패배'
                game.defender.points += def_c
                game.attacker.points -= att
            
            # 점수 변동 저장
            game.attacker.save()
            game.defender.save()
            
        game.save()
        
        return redirect('games:game_detail', pk=game.id)

# [게임 상세 페이지] : 결과 화면
@login_required
def game_detail_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'games/game_detail.html', {'game': game})

# [전체 목록] : 나의 전적 리스트
@login_required
def game_list(request):
    user = request.user
    # 내가 공격자이거나 수비자인 모든 게임 조회 (최신순)
    # id 역순(-id)을 쓰면 created_at 필드가 없어도 최신순 정렬이 됩니다.
    games = Game.objects.filter(
        Q(attacker=user) | Q(defender=user)
    ).order_by('-id')

    return render(request, 'games/game_list.html', {'games': games})

# [랭킹 페이지]
def ranking_list(request):
    User = get_user_model()
    users = User.objects.all().order_by('-points')

    if not users.exists():
        return render(request, 'games/ranking.html', {'ranking_data': []})

    max_point = users.first().points 

    ranking_data = []
    for idx, user in enumerate(users, start=1):
        percent = (user.points / max_point * 100) if max_point > 0 and user.points > 0 else 0
        ranking_data.append({
            'rank': idx,         
            'user': user,
            'percent': percent,
        })

    return render(request, 'games/ranking.html', {'ranking_data': ranking_data})

# [게임 취소]
@login_required
def cancel_duel(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if game.attacker == request.user and game.result == '진행중':
        game.delete()
    
    return redirect('games:game_list')

# [API] 상태 확인
def check_game_status(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if game.defender_card is not None:
        return JsonResponse({'finished': True})
    else:
        return JsonResponse({'finished': False})