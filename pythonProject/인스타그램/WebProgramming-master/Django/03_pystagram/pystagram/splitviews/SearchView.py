from .common import *

"""
[Pystagram] 검색결과 페이지
: 사용자가 검색창에 키워드로 검색하거나 포스트에 연결된 해시태그를 클릭했을 때 뜨는 페이지
- SearchView is linked by search.html

1. query parameter로 전달된 검색 키워드를 받아옴
2. 검색 키워드를 해시태그로 가지고 있는 포스트 수 SELECT
3. 검색 키워드를 해시태그로 가지고 있는 포스트 리스트 SELECT
4. 가져온 데이터를 search.html에 rendering
"""

def SearchView(request):
    render_page = 'search.html'
    keyword = request.GET.get('keyword')

    if not keyword.startswith("#"):
        keyword = "#" + keyword

    try:
        cursor = connection.cursor()

        # 검색 키워드를 해시태그로 가지고 있는 포스트 수
        strSql = "SELECT COUNT(*)"
        strSql += " FROM post P"
        strSql += " JOIN post_hashtag PH ON P.post_id = PH.post_id"
        strSql += " JOIN hashtag H ON PH.hashtag_id = H.hashtag_id"
        strSql += " WHERE H.keyword = (%s)"
        strSql += " ORDER BY P.time DESC"
        result = cursor.execute(strSql, (keyword,))
        data = cursor.fetchall()
        searchCount = data[0][0]


        # 검색 키워드를 해시태그로 가지고 있는 포스트 리스트
        strSql = "SELECT P.post_id, P.post_img_url"
        strSql += " FROM post P"
        strSql += " JOIN post_hashtag PH ON P.post_id = PH.post_id"
        strSql += " JOIN hashtag H ON PH.hashtag_id = H.hashtag_id"
        strSql += " WHERE H.keyword = (%s)"
        strSql += " ORDER BY P.time DESC"
        result = cursor.execute(strSql, (keyword,))
        datas = cursor.fetchall()

        searchedPosts = []
        for data in datas:
            raw_data = {'post_id': data[0],
                        'post_img_url': data[1]}

            searchedPosts.append(raw_data)

        return render(request, render_page, {'keyword': keyword, 'searchCount': searchCount, 'searchedPosts': searchedPosts})

    except:
        connection.rollback()
        print("Failed selecting in SearchView")

        messages.error(request, "포스트를 검색하는 과정에서 에러가 발생했습니다.")
        return render(request, render_page)

    finally:
        connection.close()