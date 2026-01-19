import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Game
from .utils import get_random_cards # 이전에 만든 카드 생성 함수 활용

def main_view(request):
    return render(request, 'games/main.html')

def ranking_list(request):
    User = get_user_model()
    users = User.objects.all().order_by('-points') 
    return render(request, 'ranking.html', {'users': users})

# 1. 공격하기 (명규님이 프론트를 맡으셨기에 추가가 필요합니다)
def attack_view(request):
    if request.method == 'POST':
        # 공격 로직 (백엔드 2 성유리님 파트와 협업)
        pass
    else:
        # 공격 페이지 진입 시 랜덤 카드 5장 생성 
        random_cards = get_random_cards()
        User = get_user_model()
        # 나를 제외한 다른 유저 목록 [cite: 7]
        other_users = User.objects.exclude(id=request.user.id)
        return render(request, 'games/game_attack.html', {
            'random_cards': random_cards,
            'other_users': other_users
        })

# 2. 반격하기 및 결과 판정 (명규님 기존 코드 보완)
def counter_attack(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    
    if game.defender_card is not None:
        return redirect('games:game_detail', game_id=game.id)

    if request.method == 'POST':
        selected_card = int(request.POST.get('selected_card'))
        game.defender_card = selected_card
        
        if game.attacker_card == selected_card:
            game.winner = None
        else:
            criterion = random.choice([0, 1]) 
            game.win_criterion = criterion
            
            att_card = game.attacker_card
            def_card = game.defender_card
            
            # 승자 판정 로직 [cite: 12]
            is_attacker_win = (criterion == 0 and att_card > def_card) or \
                              (criterion == 1 and att_card < def_card)
            
            if is_attacker_win:
                game.winner = game.attacker
                game.attacker.points += att_card 
                game.defender.points -= def_card 
            else:
                game.winner = game.defender
                game.defender.points += def_card 
                game.attacker.points -= att_card 
            
            game.attacker.save()
            game.defender.save()
            
        game.save()
        return redirect('games:game_detail', game_id=game.id)
    
    # GET 요청 시: 반격 페이지에 카드 5장을 뿌려줍니다 [cite: 9]
    random_cards = get_random_cards()
    return render(request, 'games/game_counter.html', {
        'game': game,
        'random_cards': random_cards
    })