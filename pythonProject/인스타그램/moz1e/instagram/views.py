from datetime import timedelta
import re
from django.contrib.auth import get_user_model
from django.contrib import messages
from instagram.forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Tag, Post
from .forms import CommentForm, PostForm

@login_required
def comment_new(request, post_pk) : 
    post = get_object_or_404(Post,pk=post_pk)
    if request.method == 'POST' : 
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid() : 
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if request.is_ajax():
                return render(request,"instagram/_comment.html",{
                    "comment":comment,
                })
            return redirect(comment.post)
    else : 
        form = CommentForm()
    
    return render(request, "instagram/comment_form.html",{
        'form' : form,
    })

@login_required
def index(request) : 
    timesince = timezone.now()-timedelta(days=100)
    post_list = Post.objects.all().filter(Q(author=request.user) | Q(author__in=request.user.following_set.all()))\
        .filter(
            created_at__gte = timesince
        )
    post_list = list(reversed(post_list))
    suggested_user_list=get_user_model().objects.all().exclude(pk=request.user.pk).exclude(pk__in=request.user.following_set.all())[:5]

    comment_form = CommentForm()
    return render(request, "instagram/Index.html",{
        "suggested_user_list" : suggested_user_list,
        "post_list" : post_list,
        "comment_form" : comment_form,
    })

@login_required
def post_new(request):
    if request.method == 'POST' : 
        form = PostForm(request.POST, request.FILES)
        if form.is_valid() : 
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.tag_set.add(*post.extract_tag_list())
            messages.success(request,"포스팅을 저장했습니다.")
            return redirect("root")
            
    else : 
        form = PostForm()

    return render(request, "instagram/post_form.html",{
        "form":form,
    })

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    comment_form = CommentForm()
    return render(request, "instagram/post_detail.html",{
        "post" : post,
        "comment_form" : comment_form,
    })

@login_required
def post_like(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.like_user_set.add(request.user)

    messages.success(request, f"포스팅 {post.pk} 좋아요")
    redirect_url = request.META.get("HTTP_REFERER","root")
    return redirect(redirect_url)

@login_required
def post_unlike(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.like_user_set.remove(request.user)

    messages.success(request, f"포스팅 {post.pk} 좋아요 취소")
    redirect_url = request.META.get("HTTP_REFERER","root")
    return redirect(redirect_url)


def user_page(request, username) : 
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    me = request.user
    post_list = Post.objects.filter(author=page_user)
    post_list_count  = post_list.count()

    follower_list = page_user.follower_set.all()
    follower_list_count = follower_list.count()

    following_list = page_user.following_set.all()
    following_list_count = following_list.count()
    
    if request.user.is_authenticated : 
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else : 
        is_follow = False
    
    return render(request, "instagram/user_page.html",{
        "page_user" : page_user,
        "post_list" : post_list,
        "post_list_count" : post_list_count,
        "is_follow" : is_follow,
        "follower_list" : follower_list,
        "following_list" : following_list,
        "me" : me,
        "follower_list_count" : follower_list_count,
        "following_list_count" : following_list_count,        
    })