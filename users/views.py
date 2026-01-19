from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm

# 1. 회원가입
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # [핵심] "ValueError: You have multiple authentication backends" 에러 방지 코드
            # 소셜 로그인 기능이 추가되면 Django가 어떤 방식으로 로그인시킬지 혼란스러워하므로,
            # "이 유저는 일반 DB(ModelBackend) 방식으로 로그인한다"고 명찰을 달아줍니다.
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            
            login(request, user)
            # 가입 성공 시 바로 게임 메인으로 이동
            return redirect('games:main')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# 2. 로그인
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # 로그인 성공 시 게임 메인으로 이동
            return redirect('games:main')
        else:
            # 로그인 실패 시 (비밀번호 틀림 등) 다시 로그인 페이지로
            # 필요하다면 에러 메시지 context 추가 가능
            return render(request, "users/login.html", {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'})
        
    return render(request, "users/login.html")

# 3. 로그아웃
def logout_view(request):
    logout(request)
    # 로그아웃 후 다시 로그인 페이지로 이동
    return redirect('users:login')