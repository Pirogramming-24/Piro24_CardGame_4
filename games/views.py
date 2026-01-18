from django.shortcuts import render

def main_view(request):
    return render(request, 'games/main_list.html') # 일단 파일명 가칭(나중에 수정하셔요)