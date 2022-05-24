from .common import *

"""
[Pystagram] 비밀번호 수정 페이지
: 사용자가 비밀번호를 수정하는 페이지
- PasswordModifyView is linked by password_modify.html

1. request.method == GET
: password_modify.html rendering

2. request.method == POST
: password_modify.html의 form 데이터를 받아와 현재 비밀번호로 자격증명 후,
자격증명에 성공한 user에 대해서만 새로운 비밀번호로 비밀번호 변경
2.1 password_modify.html의 form 데이터를 받아온다.
2.2 사용자가 입력한 현재 비밀번호가 맞는 비밀번호인가?: check_password()
    2.2.1 맞는 비밀번호
    → 새로운 비밀번호로 변경한 후, login.html로 redirect
    2.2.2 틀린 비밀번호
    → 에러 메시지와 함께 password_modify.html로 redirect
"""

@login_required
def PasswordModifyView(request):
    if request.method == "GET":
        render_page = 'password_modify.html'
        return render(request, render_page)

    else:
        user = request.user

        exist_user_pw = request.POST.get('exist_user_pw')
        new_user_pw = request.POST.get('new_user_pw')

        if user.check_password(exist_user_pw):
            user.set_password(new_user_pw)
            user.save()

            messages.success(request, '비밀번호가 변경되었습니다. 다시 로그인해주세요.')
            return redirect('accounts:pn_login')

        else:
            messages.error(request, '현재 비밀번호가 틀렸습니다. 다시 입력해주세요.')
            return redirect('accounts:pn_password_modify')