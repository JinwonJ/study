from .common import *

"""
[Pystagram] 회원 정보 수정 페이지
: 사용자가 회원 정보를 수정하는 페이지
- AccountsModifyView is linked by accounts_modify.html

1. request.method == GET
: accounts_modify.html rendering

2. request.method == POST
: accounts_modify.html 의 form 데이터를 받아와 Django 인증 시스템을 사용하여 사용자 정보 UPDATE
2.1 accounts_modify.html 의 form 데이터를 받아온다.
2.2 사용자가 프로필 이미지 파일을 업로드 한 경우,
    2.2.1 기존 프로필 이미지 파일을 삭제
    2.2.2 새로운 프로필 이미지 파일을 media 폴더에 저장한 후 저장된 경로를 return
2.3 사용자가 프로필 이미지 파일을 업로드 하지 않은 경우,
    : 기존 정보 그대로 UPDATE
"""

@login_required
def AccountsModifyView(request):
    if request.method == "GET":
        render_page = 'accounts_modify.html'
        return render(request, render_page)

    else:
        user = request.user

        profile_img_file = request.FILES.get('profile_img_file', False)
        profile_img_src = request.POST.get('profile_img_src')
        profile_msg = request.POST.get('profile_msg')
        email = request.POST.get('email')
        name = request.POST.get('name')

        try:
            user = User.objects.get(username=user.username)

            if profile_img_file is not False:
                if user.profile_img_src != "":
                    profileImageFileDelete(user.profile_img_src)

                profile_img_src = profileImageFileUpload(user, profile_img_file)

            user.profile_img_src = profile_img_src
            user.profile_msg = profile_msg
            user.email = email
            user.first_name = name

            user.save()

            return redirect('pystagram:pn_post_list', user.username)

        except:
            messages.error(request, "사용자 정보를 수정하는 과정에서 에러가 발생했습니다.")
            return redirect('accounts:pn_accounts_modify')




