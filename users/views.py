from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# 1. 회원가입
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 가입하자마자 자동 로그인
            return redirect('users:login') # 일단 로그인 페이지로 보냄 (나중에 메인으로 수정)
    else:
        form = UserCreationForm()
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

# 3. 로그아웃
def logout_view(request):
    logout(request)
    return redirect('users:login')

# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm # 1. 새로 만든 폼 임포트

def signup(request):
    if request.method == 'POST':
        # 2. 기본 폼 대신 커스텀 폼 사용
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('games:main') # 3. 가입 후 메인으로 이동
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})