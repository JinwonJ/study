from django import forms
import django
from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm
)
from .models import User

class SingupForm(UserCreationForm):
    def __init__(self,*args,**kwargs) :
        super().__init__(*args,**kwargs)
        self.fields['email'].required=True
        self.fields['first_name'].required=True
        self.fields['last_name'].required=True
    
    class Meta(UserCreationForm.Meta) : 
        model = User
        fields=['username', 'email', 'first_name', 'last_name']

    def clean_email(self) : 
        email = self.cleaned_data.get('email')
        if email : 
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 존재하는 이메일 주소입니다.")
        return email

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar','first_name','last_name','website_url','bio','phone_number','gender']

class PasswordChangeForm(AuthPasswordChangeForm) : 
    def clean_new_password2(self) :
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        #new_password2 = super().clean_new_password2()
        if old_password and new_password1 : 
            if old_password == new_password1 : 
                raise forms.ValidationError("동일한 암호로 변경할 수 없습니다.")
        return new_password1
