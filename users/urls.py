from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 1. 회원가입 (views.signup -> views.signup_view 로 변경)
    path('signup/', views.signup_view, name='signup'),

    # 2. 로그인
    path('login/', views.login_view, name='login'),

    # 3. 로그아웃
    path('logout/', views.logout_view, name='logout'),

    # [채령 추가] 소셜 로그인 URL 패턴
    # HTML에서 {% url 'users:naver' %} 라고 썼으니까 name='naver' 여야 함!
    #path('login/naver/', views.naver_login, name='naver'),
    #path('login/google/', views.google_login, name='google'),
    #path('login/kakao/', views.kakao_login, name='kakao'),
    # [채령 추가] 아래 3줄이 없어서 에러가 난 겁니다! 꼭 넣어주세요.
    # path('login/naver/', views.naver_login, name='naver'),
    # path('login/google/', views.google_login, name='google'),
    # path('login/kakao/', views.kakao_login, name='kakao'),
]   