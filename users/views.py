from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# [수정] 우리가 만든 폼을 가져옵니다!
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# 1. 회원가입
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # [중요] login(request, user) 삭제함 -> 자동 로그인 안 됨
            # [중요] 회원가입 성공 시 '로그인 페이지'로 이동
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# 2. 로그인
def login_view(request):
    # 이미 로그인한 상태라면 게임 메인으로 보냄
    if request.user.is_authenticated:
        return redirect('games:main')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('games:main')
        else:
            return render(request, "users/login.html", {"error": "아이디 또는 비밀번호가 올바르지 않습니다."})
            
    return render(request, "users/login.html")

# 3. 로그아웃
def logout_view(request):
    logout(request)
    return redirect('users:login')

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
