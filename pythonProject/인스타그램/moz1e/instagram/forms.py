from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import Comment, Post

class PostForm(forms.ModelForm) : 
    class Meta : 
        model = Post
        fields = ["photo", "caption", "location"]
        widgets = {
            "caption" : forms.Textarea,
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]
        widgets={
            "message" : forms.Textarea(attrs={"rows":2}),
        }
            
        