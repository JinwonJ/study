from .common import *

"""
[Pystagram] 로그인 페이지
: 사용자가 로그인하는 페이지
- LoginView is linked by login.html

1. request.method == GET
: login.html rendering

2. request.method == POST
: login.html의 form 데이터를 받아와 user 테이블의 데이터와 비교
2.1 아이디가 틀린 경우: 로그인 실패
2.2 비밀번호가 틀린 경우: 로그인 실패
2.3 둘 다 맞는 경우: 로그인 성공
"""

def LoginView(request):
    if request.method == 'GET':
        render_page = "login.html"
        return render(request, render_page)

    else:
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')


        user = authenticate(request, username=user_id, password=user_pw)

        if user is not None:
            login(request, user=user)
            return redirect('pystagram:pn_main')

        else:
            messages.error(request, '아이디 혹은 비밀번호가 틀렸습니다. 다시 입력해주세요.')
            return redirect('accounts:pn_login')