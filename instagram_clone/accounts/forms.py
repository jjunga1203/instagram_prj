from typing import Any
from django.db import models

from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django import forms

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['password1'].help_text = '' # "<br>6자리 이상, 숫자/문자/기호문자 포함해주세요"
        self.fields['password1'].widget = forms.TextInput(attrs={'id':'password1', 'type':'password', 'placeholder': '6자리 이상, 숫자/문자/기호문자 포함해주세요','class': 'placeholder-message'})
        self.fields['password1'].label = ''
        del self.fields['password2']


    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        # 'profile_img', email
        # fields = ('username', 'alias_name', 'real_name','introduce', 'gender', 'is_notify')
        fields = ('username', 'alias_name', 'real_name', 'password1')
      
        widgets = {
            'real_name':forms.TextInput(attrs={"placeholder" : "성명을 입력하세요", 'class': 'placeholder-message'}),
            'alias_name':forms.TextInput(attrs={"placeholder" : "사용자 이름을 입력하세요", 'class': 'placeholder-message'}),
            'username': forms.TextInput(attrs={'placeholder':'핸드폰번호나 이메일을 입력해주세요', 'class': 'placeholder-message'}),
        }
        labels = {
            'username' : '',
            'real_name' : '',
            'alias_name' : '',
            'password1': '',
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        # 'profile_img', email
        fields = ('real_name','introduce', 'gender', 'is_notify')
      
        widgets = {
            'is_notify': forms.CheckboxInput(),
            'introduce':forms.TextInput(attrs={"placeholder" : "자기소개를 입력하세요"}),
        }
        labels = {
            'gender' : '성별',
            'introduce' : '자기소개',
            'is_notify' : '알림여부',
            # 'password' : '비밀번호',
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={'placeholder': '가입한 핸드폰번호/이메일 입력'})
    )
    password = forms.CharField(
        max_length=100,
        label='',
        widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'})
    )