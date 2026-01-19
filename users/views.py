from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# [수정] 우리가 만든 폼을 가져옵니다!
from .forms import CustomUserCreationForm

# 1. 회원가입
def signup(request):
    if request.method == 'POST':
        # [수정] UserCreationForm -> CustomUserCreationForm으로 변경
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:login') 
    else:
        # [수정] 여기도 변경
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# 2. 로그인
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/') # 메인 페이지로 이동 (지금은 에러날 수 있음)
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# [채령 추가] 소셜 로그인 임시 함수 (에러 방지용 껍데기) 이거 런서버가 계속 안되서 아무 내용없는 함수 넣었어요
#소셜로그인 구현 하실때 지우고 하시거나 해주세요
def naver_login(request):
    return redirect('users:login') 

def google_login(request):
    return redirect('users:login')

def kakao_login(request):
    return redirect('users:login')

# 3. 로그아웃
def logout_view(request):
    logout(request)
    return redirect('users:login')