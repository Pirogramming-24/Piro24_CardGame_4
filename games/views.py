import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .models import Game

# 1. 유틸리티 함수
def get_random_cards():
    """1부터 10까지의 숫자 중 랜덤으로 5개를 뽑아 정렬하여 반환"""
    cards = random.sample(range(1, 11), 5)
    return sorted(cards)

# 2. 뷰 함수

# [메인 페이지] : 전적 리스트 + 대결 요청 모달 확인
def main_view(request):
    if request.user.is_authenticated:
        # 1) 전적 리스트 (내가 공격했거나 방어했던 모든 게임)
        games = Game.objects.filter(attacker=request.user) | Game.objects.filter(defender=request.user)
        games = games.order_by('-created_at')
        
        # 2) [중요] 나에게 온 '진행중'인 대결 요청 확인 (모달용)
        # defender가 '나'이고, 결과가 아직 '진행중'인 게임 중 가장 최신 것
        pending_game = Game.objects.filter(defender=request.user, result='진행중').first()
        
        context = {
            'games': games,
            'pending_game': pending_game 
        }
        return render(request, 'games/game_list.html', context)
    else:
        # 로그인 안 한 유저 -> 대문 페이지
        return render(request, 'games/main.html')

# [API] 상태 확인용 (공격자 대기화면에서 1초마다 호출)
def check_game_status(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # defender_card가 채워졌다면(반격 완료), 끝난 것으로 간주
    if game.defender_card is not None:
        return JsonResponse({'finished': True})
    else:
        return JsonResponse({'finished': False})

# [공격하기] : 게임 생성
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
        # [디버깅] 요청 확인
        print("============== 공격 요청 도착! ==============")

        defender_id = request.POST.get('defender') 
        card_picked = request.POST.get('selected_card') 

        print(f"받은 데이터 - 상대방: {defender_id}, 카드: {card_picked}")

        # 유효성 검사
        if not defender_id or not card_picked:
             print("데이터 누락으로 인해 리다이렉트 됩니다.")
             return redirect('games:game_attack')

        try:
            defender = User.objects.get(id=defender_id)
            
            # 게임 DB 생성
            game = Game.objects.create(
                attacker=request.user,
                defender=defender,
                attacker_card=int(card_picked),
                result='진행중'
            )
            
            # 공격자는 대기 화면(loading)으로 이동하며 game.id를 전달
            return render(request, 'games/game_loading.html', {'game_id': game.id})
            
        except User.DoesNotExist:
            return redirect('games:game_attack')

# 3. 비즈니스 로직 (반격)

# [반격하기] : 결과 판정 및 점수 계산
@login_required
def counter_attack(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # 이미 방어한 게임이면(중복 반격 방지) 결과 페이지로 이동
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
        
        # 카드 선택 안 했을 경우 재시도
        if not selected_card:
            return redirect('games:counter_attack', game_id=game.id)

        selected_card = int(selected_card)
        game.defender_card = selected_card
        
        # --- 승패 판정 로직 ---
        if game.attacker_card == selected_card:
            game.winner = None 
            game.result = '무승부'
        else:
            # 승리 기준 랜덤 결정 (0: 큰 수 승리, 1: 작은 수 승리)
            criterion = random.choice([0, 1])
            game.win_criterion = criterion
            
            att_card = game.attacker_card
            def_card = game.defender_card
            
            # 승리 조건 검사
            is_attacker_win = (criterion == 0 and att_card > def_card) or \
                              (criterion == 1 and att_card < def_card)
            
            if is_attacker_win:
                game.winner = game.attacker
                game.result = '승리' # 공격자 기준
                game.attacker.points += att_card
                game.defender.points -= def_card
            else:
                game.winner = game.defender
                game.result = '패배' # 공격자 기준
                game.defender.points += def_card
                game.attacker.points -= att_card
            
            # 변경된 점수 저장
            game.attacker.save()
            game.defender.save()
            
        game.save()
        
        # 수비자는 반격이 끝나면 바로 결과 페이지(Detail)로 이동
        return redirect('games:game_detail', pk=game.id)

# [랭킹 페이지]
def ranking_list(request):
    User = get_user_model()
    users = User.objects.all().order_by('-points')

    # 1등 점수 (그래프 비율 계산용)
    max_point = users[0].points if users.exists() else 0

    ranking_data = []
    for idx, user in enumerate(users, start=1):
        # 0으로 나누기 방지
        percent = (user.points / max_point * 100) if max_point > 0 else 0

        ranking_data.append({
            'rank': idx,         
            'user': user,
            'percent': percent,
        })

    return render(
        request,
        'games/ranking.html',
        {'ranking_data': ranking_data}
    )

# [게임 상세 페이지] : 결과 화면
def game_detail_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'games/game_detail.html', {'game': game})

# [유저 관련] : 로그인/회원가입
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # 로그인 성공 시 게임 리스트(메인)로 이동
            return redirect('games:main')
            
    return render(request, "users/login.html")

def signup_view(request):
    return render(request, "users/signup.html")

@login_required
def cancel_duel(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # 안전장치: 요청한 사람이 공격자가 맞는지, 아직 진행중인지 확인
    if game.attacker == request.user and game.result == '진행중':
        game.delete() # DB에서 게임 삭제
    
    # 메인 페이지로 복귀
    return redirect('games:main')