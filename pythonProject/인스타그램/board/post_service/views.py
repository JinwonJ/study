from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import LoginForm
from django.contrib import auth


def post_list(request):
    page_data = Paginator(Post.objects.all(), 5)
    page = request.GET.get('page', 1)

    try:
        posts = page_data.page(page)
    except PageNotAnInteger:
        posts = page_data.page(1)
    except EmptyPage:
        posts = page_data.page(page_data.num_pages)

    return render(request, 'post_list.html', {'post_list': posts, 'current_page': int(page),
                                              'total_page': range(1, page_data.num_pages)})


def login(request):
    return render(request, 'login_form.html', {'login_form': LoginForm})


def login_validate(request):
    login_form_data = LoginForm(request.POST)

    if login_form_data.is_valid():
        user = auth.authenticate(username=request.POST['id'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/board/')
        else: return HttpResponse('사용자가 없거나 비밀번호를 잘못 누르셨습니다.')
    else:
        return HttpResponse('로그인 폼이 비정상적입니다.')
    return HttpResponse('알수 없는 오류입니다.')

