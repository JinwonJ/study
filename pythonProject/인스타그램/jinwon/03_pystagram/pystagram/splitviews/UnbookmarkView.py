from .common import *

"""
[Pystagram] 북마크 취소 뷰
: 사용자가 포스트의 컬렉션 버튼을 누르면 사용자의 컬렉션에 저장되는 뷰
- BookmarkView is linked by <컬렉션 버튼> in main.html, post_detail.html
- Ajax

1. 현재 로그인된 유저가 컬렉션을 누른 포스트의 post_id와 현재 유저의 아이디로 bookmark에 데이터 DELETE
2. 성공 여부를 return
"""

@login_required
def UnbookmarkView(request, post_id):
    user = request.user
    try:
        cursor = connection.cursor()

        strSql = "DELETE FROM bookmark"
        strSql += " WHERE post_id = (%s)"
        strSql += " AND user_id = (%s)"
        result = cursor.execute(strSql, (post_id, user.username))

        return HttpResponse(json.dumps({'result': '200',}), content_type="application/json")

    except:
        connection.rollback()
        print("Failed deleting in UnbookmarkView")

    finally:
        connection.close()