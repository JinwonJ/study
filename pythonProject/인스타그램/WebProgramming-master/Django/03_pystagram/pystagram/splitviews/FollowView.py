from .common import *

"""
[Pystagram] 팔로우 뷰
: 사용자가 팔로우 버튼이 클릭된 계정을 팔로우 할 수 있는 뷰
- FollowView is linked by <팔로우 버튼> in post_list.html
- (200309 수정) Ajax

(200309 수정)
1. 현재 사용자와 팔로우 대상 계정의 아이디를 이용해 following 테이블에 INSERT
2. post_list.html의 팔로우 수 변경을 위한 팔로우 수 SELECT
3. 팔로우 수 return
"""

@login_required
def FollowView(request, following_id):
    user = request.user

    try:
        cursor = connection.cursor()

        strSql = "INSERT INTO following(user_id, following_id)"
        strSql += " VALUES(%s, %s)"
        result = cursor.execute(strSql, (user.username, following_id))

        # 팔로워 수
        strSql = "SELECT COUNT(user_id)"
        strSql += " FROM following"
        strSql += " WHERE following_id = (%s)"

        result = cursor.execute(strSql, (following_id,))
        data = cursor.fetchall()
        followerCount = data[0][0]

        return HttpResponse(json.dumps({'result': '200', 'followerCount': followerCount}), content_type="application/json")

    except:
        connection.rollback()
        print("Failed inserting in FollowView")

    finally:
        connection.close()