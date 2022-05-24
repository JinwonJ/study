from accounts.forms import SignupForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"회원가입을 환영")
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'account/signup_form.html',{})



