from .common import *

"""
[Pystagram] 좋아요 취소 뷰
: 사용자가 포스트의 좋아요 버튼을 누르면 해당 포스트의 좋아요 개수에 반영하는 뷰
- UnlikePostView is linked by <좋아요 버튼> in main.html, post_detail.html
- Ajax

1. 현재 로그인된 유저가 좋아요를 누른 포스트의 post_id와 현재 유저의 아이디로 like_post에 데이터 DELETE
2. 선택된 포스트의 변경된 좋아요 개수를 SELECT
3. 좋아요 개수를 return
"""

@login_required
def UnlikePostView(request, post_id):
    user = request.user
    try:
        cursor = connection.cursor()

        strSql = "DELETE FROM like_post"
        strSql += " WHERE post_id = (%s)"
        strSql += " AND user_id = (%s)"
        result = cursor.execute(strSql, (post_id, user.username))

        strSql = "SELECT COUNT(*)"
        strSql += " FROM like_post"
        strSql += " WHERE post_id = (%s)"
        result = cursor.execute(strSql, (post_id,))
        data = cursor.fetchall()

        likeCount = data[0][0]

        return HttpResponse(json.dumps({'result': '200', 'likeCount': likeCount}), content_type="application/json")

    except:
        connection.rollback()
        print("Failed working in UnlikePostView")

    finally:
        connection.close()