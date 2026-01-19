import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.db.models import Q  # [중요] 이거 없으면 에러 납니다!
from .models import Game

# 1. 유틸리티 함수
def get_random_cards():
    """1부터 10까지의 숫자 중 랜덤으로 5개를 뽑아 정렬하여 반환"""
    cards = random.sample(range(1, 11), 5)
    return sorted(cards)

# 2. 뷰 함수

# [메인 페이지] : 전적 리스트 + 대결 요청 모달 확인
def main_view(request):
    # 1. 로그인 한 사람인가? (True)
    if request.user.is_authenticated:
        games = Game.objects.filter(attacker=request.user) | Game.objects.filter(defender=request.user)
        games = games.order_by('-created_at')
        
        pending_game = Game.objects.filter(defender=request.user, result='진행중').first()
        
        context = {
            'games': games,
            'pending_game': pending_game 
        }
        # [수정] 원래 'games/game_list.html' 이었던 것을 -> 'games/logined.html'로 변경!
        return render(request, 'games/main_logined.html', context)

    # 2. 로그인 안 한 사람인가? (False)
    else:
        # 대문 페이지
        return render(request, 'games/main.html')

# [API] 상태 확인용
def check_game_status(request, game_id):
    game = get_object_or_404(Game, id=game_id)
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
        
        pending_game = Game.objects.filter(defender=request.user, result='진행중').first()
        
        context = {
            'random_cards': random_cards, 
            'other_users': other_users,
            'pending_game': pending_game
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

# [반격하기]
@login_required
def counter_attack(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # 이미 방어한 게임이면 결과 페이지로
    if game.defender_card is not None:
        return redirect('games:game_detail', pk=game.id)

    if request.method == 'GET':
        random_cards = random.sample(range(1, 11), 5) # 유틸함수 써도 됨
        return render(request, 'games/game_counter.html', {
            'game': game,
            'random_cards': sorted(random_cards)
        })

    elif request.method == 'POST':
        selected_card = request.POST.get('selected_card')
        if not selected_card:
            return redirect('games:counter_attack', game_id=game.id)

        selected_card = int(selected_card)
        game.defender_card = selected_card
        
        # 승패 판정 로직
        if game.attacker_card == selected_card:
            game.winner = None 
            game.result = '무승부' # [중요] 상태를 '진행중'에서 변경
        else:
            criterion = random.choice([0, 1])
            game.win_criterion = criterion
            
            att = game.attacker_card
            def_c = game.defender_card
            
            # 0: 큰 수 승리, 1: 작은 수 승리
            is_att_win = (criterion == 0 and att > def_c) or (criterion == 1 and att < def_c)
            
            if is_att_win:
                game.winner = game.attacker
                game.result = '승리' # 공격자 기준 결과 텍스트 (혹은 '종료'로 통일해도 됨)
                game.attacker.points += att
                game.defender.points -= def_c
            else:
                game.winner = game.defender
                game.result = '패배'
                game.defender.points += def_c
                game.attacker.points -= att
            
            game.attacker.save()
            game.defender.save()
            
        game.save() # DB 저장 필수
        
        return redirect('games:game_detail', pk=game.id)

# [랭킹 페이지]
def ranking_list(request):
    User = get_user_model()
    users = User.objects.all().order_by('-points')

    if not users.exists():
        return render(request, 'games/ranking.html', {'ranking_data': []})

    max_point = users.first().points
    min_point = users.last().points

    # 모든 점수가 같은 경우 (0으로 나누기 방지)
    range_point = max_point - min_point

    ranking_data = []
    for idx, user in enumerate(users, start=1):
        if range_point > 0:
            percent = (user.points - min_point) / range_point * 100
        else:
            percent = 100  # 전부 같은 점수면 동일 높이

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

# [게임 취소]
@login_required
def cancel_duel(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # 본인이 공격자이고, 아직 '진행중'일 때만 삭제 가능
    if game.attacker == request.user and game.result == '진행중':
        game.delete()
    
    # 삭제 후엔 리스트로 돌아가는 게 자연스러움
    return redirect('games:game_list')

# [게임 리스트]
@login_required
def game_list(request):
    user = request.user

    # Q 객체를 사용해 내가 공격자거나 수비자인 게임 조회
    games = Game.objects.filter(
        Q(attacker=user) | Q(defender=user)
    ).order_by('-created_at')

    # 템플릿 렌더링
    return render(request, 'games/game_list.html', {
        'games': games,
        # pending_game은 리스트 내에서 반복문으로 처리되므로 굳이 안 보내도 됩니다.
    })