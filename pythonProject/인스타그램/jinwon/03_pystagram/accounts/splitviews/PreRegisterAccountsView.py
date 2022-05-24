from .common import *

"""
[Pystagram] 회원가입 페이지
: 사용자가 회원가입하는 페이지
- RegisterAccountsView is linked by reg_accounts.html

1. request.method == GET
: reg_accounts.html rendering

2. request.method == POST
: reg_accounts.html의 form 데이터를 받아와 user 테이블에 새로운 사용자 INSERT
- 비밀번호 hash를 위해 hashing_password()를 호출
- hash된 비밀번호를 DB에 INSERT
"""

def PreRegisterAccountsView(request):
    if request.method == 'GET':
        renderPage = 'reg_accounts.html'
        return render(request, renderPage)

    else:
        email = request.POST.get('email')
        name = request.POST.get('name')
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')

        try:
            cursor = connection.cursor()

            strSql = "SELECT user_id"
            strSql += " FROM user"
            strSql += " WHERE user_id = (%s)"
            result = cursor.execute(strSql, (user_id,))
            datas = cursor.fetchall()

            if len(datas) != 0:
                messages.error(request, '이미 존재하는 아이디입니다. 다른 아이디를 사용해주세요.')
                return redirect('accounts:pn_reg_accounts')

            else:
                # 비밀번호 hash를 위해 호출
                salt, hashed_pw = hashing_password(user_pw)

                strSql = "INSERT INTO user(user_id, user_pw, name, email, salt)"
                strSql += " VALUES(%s, %s, %s, %s, %s)"

                result = cursor.execute(strSql, (user_id, hashed_pw, name, email, salt))
                connection.commit()

                messages.success(request, '회원가입이 되었습니다. 로그인을 해주세요.')
                return redirect('accounts:pn_login')

        except:
            connection.rollback()
            print("Failed inserting in RegisterAccountsView")

            messages.error(request, '회원가입을 하는 과정에서 에러가 발생했습니다. 다시 시도해주세요.')
            return redirect('accounts:pn_reg_accounts')

        finally:
            connection.close()