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
- 사용자가 입력한 비밀번호와 사용자 ID의 row에서 가져온 salt를 합침
- 합친 문자열을 hash하여 DB의 user_pw와 비교
2.3 둘 다 맞는 경우: 로그인 성공
"""

def PreLoginView(request):
    if request.method == 'GET':
        render_page = "login.html"
        return render(request, render_page)

    else:
        user_id = request.POST.get('user_id')
        user_pw = request.POST.get('user_pw')

        try:
            cursor = connection.cursor()

            strSql = "SELECT user_id, user_pw, salt"
            strSql += " FROM user"
            strSql += " WHERE user_id = (%s)"

            result = cursor.execute(strSql, (user_id,))
            datas = cursor.fetchall()
            connection.commit()

            # 2.1 아이디가 틀린 경우: 로그인 실패
            if len(datas) == 0:
                messages.error(request, '아이디나 비밀번호가 일치하지 않습니다. 다시 입력해주세요.')
                return redirect('accounts:pn_login')

            else:
                reg_id = datas[0][0]
                reg_pw = datas[0][1]
                salt = datas[0][2]

                hash = pbkdf2(user_pw, salt, 10000, digest=hashlib.sha256)
                hashed_pw = base64.b64encode(hash).decode('ascii').strip()

                # 2.2 비밀번호가 틀린 경우: 로그인 실패
                if str(hashed_pw) != reg_pw:
                    messages.error(request, '아이디나 비밀번호가 일치하지 않습니다. 다시 입력해주세요.')
                    return redirect('accounts:pn_login')

                # 2.3 둘 다 맞는 경우: 로그인 성공
                else:
                    request.session['user_id'] = reg_id
                    return redirect('pystagram:pn_main')

        except:
            connection.rollback()
            print("Failed inserting in RegisterAccountsView")

            messages.error(request, '로그인하는 과정에서 에러가 발생했습니다. 다시 시도했습니다.')
            return redirect('accounts:pn_login')

        finally:
            connection.close()