from .common import *

"""
[Pystagram] 포스트 업로드 페이지
: 사용자가 포스트를 업로드하는 페이지
- PostUploadView is linked by post_create.html

1. request.method == GET
: post_create.html rendering

2. request.method == POST
: post_create.html 의 form 데이터를 받아와 post 테이블에 데이터 INSERT
2.1 post_create.html 의 form 데이터를 받아온다.
2.2 post_img_url = fileUpload(user, postImg)
    - 사용자가 올린 사진 파일을 media 폴더에 저장한 후 저장된 경로를 return
2.3 post 테이블에 데이터 INSERT
2.4 방금 INSERT한 포스트의 해시태그 데이터 INSERT
    2.4.1 hashtag 테이블에 등록된 해시태그인지 확인
    2.4.2 등록되지 않은 해시태그인 경우: hashtag 테이블과 post_hashtag 테이블 모두 INSERT
    2.4.3 등록된 해시태그인 경우, post_hashtag 테이블에만 INSERT
"""

@login_required
def PostUploadView(request):
    user = request.user

    if request.method == 'GET':
        render_page = 'post_create.html'
        return render(request, render_page)

    else:
        content = request.POST.get('content')
        postImg = request.FILES.get('postImg')
        hashtags = request.POST.get('hashtag')
        hashtags = hashtags.split(" ")

        post_img_url = fileUpload(user, postImg)

        try:
            cursor = connection.cursor()

            strSql = "INSERT INTO post(user_id, post_img_url, content)"
            strSql += " VALUES(%s, %s, %s)"
            result = cursor.execute(strSql, (user.username, post_img_url, content))
            insertedPostId = cursor.lastrowid

            for tag in hashtags:
                if tag.startswith("#"):
                    strSql = "SELECT hashtag_id FROM hashtag WHERE keyword = (%s)"
                    result = cursor.execute(strSql, (tag,))
                    data = cursor.fetchall()

                    if result == 0:
                        strSql = "INSERT INTO hashtag(keyword)"
                        strSql += " VALUES(%s)"
                        result = cursor.execute(strSql, (tag,))
                        insertedHashtagId = cursor.lastrowid

                        strSql = "INSERT INTO post_hashtag(post_id, hashtag_id)"
                        strSql += " VALUES(%s, %s)"
                        result = cursor.execute(strSql, (insertedPostId, insertedHashtagId))

                    else:
                        strSql = "INSERT INTO post_hashtag(post_id, hashtag_id)"
                        strSql += " VALUES(%s, %s)"
                        result = cursor.execute(strSql, (insertedPostId, data[0][0]))


            return redirect('pystagram:pn_main')

        except:
            connection.rollback()
            print("Failed inserting in PostUploadView")

            messages.error(request, "포스트를 업로드하는 과정에서 에러가 발생했습니다. 다시 시도해주세요.")
            return redirect('pystagram:pn_post_upload')

        finally:
            connection.close()