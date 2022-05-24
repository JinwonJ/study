from .common import *

"""
[Pystagram] 좋아요 뷰
: 사용자가 포스트의 좋아요 버튼을 누르면 해당 포스트의 좋아요 개수에 반영하는 뷰
- LikePostView is linked by <좋아요 버튼> in main.html, post_detail.html
- Ajax

1. 현재 로그인된 유저가 좋아요를 누른 포스트의 post_id와 현재 유저의 아이디로 like_post에 데이터 INSERT
2. 선택된 포스트의 변경된 좋아요 개수를 SELECT
3. 좋아요 개수를 return
"""

@login_required
def LikePostView(request, post_id):
    user = request.user
    try:
        cursor = connection.cursor()

        strSql = "INSERT INTO like_post(post_id, user_id)"
        strSql += " VALUES(%s, %s)"
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
        print("Failed working in LikePostView")

    finally:
        connection.close()