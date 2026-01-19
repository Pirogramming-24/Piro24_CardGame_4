import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Game
from django.contrib.auth import authenticate, login

# 1. 유틸리티 함수
def get_random_cards():
    cards = random.sample(range(1, 11), 5)
    return sorted(cards)

@login_required
def mainlogined_view(request):
    return render(request, 'games/main_logined.html')

# 1. 랭킹 페이지 조회 (백엔드 3)
# 2. 뷰 함수 (페이지 연결)
# 메인 페이지
def main_view(request):
    if request.user.is_authenticated:
        # 로그인 유저 → 로그인 메인
        return render(request, 'games/main_logined.html')
    else:
        # 비로그인 유저 → 대문
        return render(request, 'games/main.html')


# 공격하기 (게임 생성)
@login_required
def attack_view(request):
    User = get_user_model()
    
    if request.method == 'GET':
        cards = get_random_cards()
        users = User.objects.exclude(id=request.user.id)
        
        context = {
            'cards': cards,
            'users': users
        }
        # 파일명 game_attack.html로 변경
        return render(request, 'games/game_attack.html', context)
    
    elif request.method == 'POST':
        defender_id = request.POST.get('defender_id')
        card_picked = request.POST.get('card_picked') 

        defender = get_object_or_404(User, id=defender_id)

        # 게임 생성 (DB 저장)
        Game.objects.create(
            attacker=request.user,
            defender=defender,
            attacker_card=int(card_picked),
            defender_card=None,
            win_criterion=None,
            winner=None,
            result='진행중'
        )

        return redirect('games:main')

# 랭킹 페이지 조회
def ranking_list(request):
    User = get_user_model()
    users = User.objects.all().order_by('-points')

    max_point = users[0].points if users.exists() else 0

    ranking_data = []
    for idx, user in enumerate(users, start=1):
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




# 게임 상세 페이지
def game_detail_view(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'games/game_detail.html', {'game': game})


# 3. 비즈니스 로직 (반격)

# 반격하기 및 결과 판정
def counter_attack(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    # 이미 반격이 완료된 게임이면 상세 페이지로 이동
    if game.defender_card is not None:
        return redirect('games:game_detail', pk=game.id) 

    if request.method == 'POST':
        selected_card = int(request.POST.get('selected_card'))
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
            
            # 점수 저장
            game.attacker.save()
            game.defender.save()
            
        game.save()
        return redirect('game_detail', game_id=game.id) # 반격 후 상세 페이지로 
    

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/games/loginedmain/')
    return render(request, "users/login.html")


def signup_view(request):
    return render(request, "users/signup.html")

def game_list_view(request):
    return render(request, "games/game_list.html")

@login_required
def game_list_view(request):
    games = (
        Game.objects.filter(attacker=request.user)
        | Game.objects.filter(defender=request.user)
    ).order_by('-created_at')

    return render(request, 'games/game_list.html', {'games': games})

