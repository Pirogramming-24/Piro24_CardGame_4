from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm

# 1. 회원가입
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # [핵심] 소셜 로그인 충돌 방지 (일반 DB 로그인 명시)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            # 가입 후 자동 로그인
            login(request, user)
            
            # [수정] 가입 성공 시 'Start 버튼'이 있는 메인으로 이동
            return redirect('games:main_logined') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# 2. 로그인
def login_view(request):
    # 이미 로그인한 상태라면 바로 Start 화면으로 보냄
    if request.user.is_authenticated:
        return redirect('games:main_logined')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # [수정] 로그인 성공 시 'Start 버튼'이 있는 메인으로 이동
            return redirect('games:main_logined')
        else:
            # 로그인 실패 시 에러 메시지 표시
            return render(request, "users/login.html", {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'})
            
    return render(request, "users/login.html")

# 3. 로그아웃
def logout_view(request):
    logout(request)
    # 로그아웃 후 다시 로그인 페이지로 이동
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