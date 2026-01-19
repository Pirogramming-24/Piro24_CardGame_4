import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from django.urls import reverse
from .models import Game

# 1. 유틸리티 함수
def get_random_cards():
    cards = random.sample(range(1, 11), 5)
    return sorted(cards)

# 2. 뷰 함수

# 메인 페이지 (모달 기능 포함)
def main_view(request):
    if request.user.is_authenticated:
        # 1) 전적 리스트
        games = Game.objects.filter(attacker=request.user) | Game.objects.filter(defender=request.user)
        games = games.order_by('-created_at')
        
        # 2) [중요] 나에게 온 '진행중'인 대결 요청 확인 (모달용)
        pending_game = Game.objects.filter(defender=request.user, result='진행중').first()
        
        context = {
            'games': games,
            'pending_game': pending_game 
        }
        return render(request, 'games/game_list.html', context)
    else:
        # 로그인 안 한 유저 -> 대문
        return render(request, 'games/main.html')

# [API] 상태 확인용 (공격자 대기화면에서 사용)
def check_game_status(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # defender_card가 채워졌다면(반격 완료), 끝난 것으로 간주
    if game.defender_card is not None:
        return JsonResponse({'finished': True})
    else:
        return JsonResponse({'finished': False})

# 공격하기 (게임 생성)
@login_required
def attack_view(request):
    User = get_user_model()
    
    if request.method == 'GET':
        random_cards = get_random_cards()
        other_users = User.objects.exclude(id=request.user.id)
        context = {
            'random_cards': random_cards, 
            'other_users': other_users
        }
        return render(request, 'games/game_attack.html', context)
    
    elif request.method == 'POST':
        # [디버깅] 터미널 출력
        print("============== 공격 요청 도착! ==============")

        defender_id = request.POST.get('defender') 
        card_picked = request.POST.get('selected_card') 

        print(f"받은 데이터 - 상대방: {defender_id}, 카드: {card_picked}")

        # 데이터 누락 체크
        if not defender_id or not card_picked:
             print("데이터 누락으로 인해 리다이렉트 됩니다.")
             return redirect('games:game_attack')

        try:
            defender = User.objects.get(id=defender_id)
            
            # 게임 생성
            game = Game.objects.create(
                attacker=request.user,
                defender=defender,
                attacker_card=int(card_picked),
                result='진행중'
            )
            
            # 공격자는 대기 화면(loading)으로 이동하며 game.id를 가져감
            return render(request, 'games/game_loading.html', {'game_id': game.id})
            
        except User.DoesNotExist:
            return redirect('games:game_attack')

# 반격하기 및 결과 판정
@login_required
def counter_attack(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # 이미 방어한 게임이면 결과 페이지로 이동
    if game.defender_card is not None:
        return redirect('games:game_detail', pk=game.id)

    # [GET 추가] 페이지 접속 시 (이게 없으면 반격 화면이 안 뜹니다)
    if request.method == 'GET':
        random_cards = get_random_cards()
        context = {
            'game': game,
            'random_cards': random_cards
        }
        return render(request, 'games/game_counter.html', context)

    # [POST] 카드 선택 후 제출 시
    elif request.method == 'POST':
        selected_card = request.POST.get('selected_card')
        
        # 카드 선택 안 했을 경우 방어
        if not selected_card:
            return redirect('games:counter_attack', game_id=game.id)

        selected_card = int(selected_card)
        game.defender_card = selected_card
        
        # [결과 판정 로직]
        if game.attacker_card == selected_card:
            game.winner = None 
            game.result = '무승부'
        else:
            # 승리 기준 랜덤 결정 (0: 큰 수 승리, 1: 작은 수 승리)
            criterion = random.choice([0, 1])
            game.win_criterion = criterion
            
            att_card = game.attacker_card
            def_card = game.defender_card
            
            is_attacker_win = (criterion == 0 and att_card > def_card) or \
                              (criterion == 1 and att_card < def_card)
            
            if is_attacker_win:
                game.winner = game.attacker
                game.result = '승리'
                game.attacker.points += att_card
                game.defender.points -= def_card
            else:
                game.winner = game.defender
                game.result = '패배'
                game.defender.points += def_card
                game.attacker.points -= att_card
            
            # 포인트 저장
            game.attacker.save()
            game.defender.save()
            
        game.save()
        
        # 수비자는 반격이 끝나면 바로 결과 페이지(Detail)로 이동
        return redirect('games:game_detail', pk=game.id)

# 랭킹 페이지 조회
def ranking_list(request):
    User = get_user_model()
    users = User.objects.all().order_by('-points')
    return render(request, 'games/ranking.html', {'users': users})

# 게임 상세 페이지
def game_detail_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'games/game_detail.html', {'game': game})

# 유저 관련 (로그인/회원가입 - 필요 시 사용)
def login_view(request):
    return render(request, "users/login.html")

def signup_view(request):
    return render(request, "users/signup.html")