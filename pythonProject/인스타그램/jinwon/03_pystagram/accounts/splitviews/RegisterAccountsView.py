from .common import *

"""
[Pystagram] 회원가입 페이지
: 사용자가 회원가입하는 페이지
- RegisterAccountsView is linked by reg_accounts.html

1. request.method == GET
: reg_accounts.html rendering

2. request.method == POST
: reg_accounts.html의 form 데이터를 받아와 user 테이블에 새로운 사용자 INSERT
"""

def RegisterAccountsView(request):
    if request.method == 'GET':
        renderPage = 'reg_accounts.html'
        return render(request, renderPage)

    else:
        email = request.POST.get('email')
        name = request.POST.get('name')
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')

        try:
            user = User.objects.get(username=user_id)

            messages.error(request, '이미 존재하는 아이디입니다. 다른 아이디를 사용해주세요.')
            return redirect('accounts:pn_reg_accounts')

        except ObjectDoesNotExist:
            user = User.objects.create_user(username=user_id, password=user_pw, email=email, first_name=name)
            messages.success(request, '회원가입이 되었습니다. 로그인을 해주세요.')
            return redirect('accounts:pn_login')