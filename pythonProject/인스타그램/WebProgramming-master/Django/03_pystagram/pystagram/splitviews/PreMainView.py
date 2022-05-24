from .common import *

"""
[Pystagram] 메인 페이지
: 사용자의 포스트, 사용자가 팔로우한 계정의 포스트를 볼 수 있는 페이지
- PreMainView is linked by main.html

1. 세션에 로그인한 사용자의 user_id가 있는 경우
: 메인페이지 render

2. 세션에 로그인한 사용자의 user_id가 없는 경우
: 로그인 페이지로 redirect
"""

def PreMainView(request):
    isSession = request.session.get('user_id', False)

    if isSession is not False:
        render_page = "main.html"
        return render(request, render_page, {'user_id': isSession})

    else:
        return redirect('accounts:pn_login')