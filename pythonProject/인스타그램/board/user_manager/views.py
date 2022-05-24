from django.shortcuts import render, redirect
from .forms import LoginForm, JoinForm
from django.contrib import auth
from django.http import HttpResponse


def login(request):
    return render(request, 'login_form.html', {'login_form': LoginForm()})


def login_validate(request):
    login_form_data = LoginForm(request.POST)
    if login_form_data.is_valid():
        user = auth.authenticate(username=request.POST['id'], password=request.POST['password'])
        if user is not None:
            if user.is_active: auth.login(request, user)
            return redirect('/board/')
        else:
            return HttpResponse('사용자가 없거나 비밀번호를 잘못 누르셨습니다.')
    else:
        return HttpResponse('로그인 폼이 비정상적입니다.')
    return HttpResponse('알수 없는 오류입니다.')

def join_page(requeset):
    return HttpResponse('회원가입')


def join_page(request):
    if request.method =="POST":
        form_data = JoinForm(request.POST)
        if form_data.is_valid():
            username = form_data.cleaned_data['id']
            password = form_data.cleaned_data['password']

            User = auth.get_user_model()
            User.objects.create_user(username=username, password=password)

            return redirect('/user/login/')
    else:
        form_data = JoinForm()

    return render(request, 'join_page.html', {'join_form':form_data})