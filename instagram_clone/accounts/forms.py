from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        # 'profile_img', email
        fields = ('username', 'alias_name', 'real_name','introduce', 'gender', 'is_notify')
      
        widgets = {
            'is_notify': forms.CheckboxInput(),
            'introduce':forms.TextInput(attrs={"placeholder" : "자기소개를 입력하세요"}),
            'username': forms.TextInput(attrs={'placeholder':'핸드폰번호나 이메일을 입력해주세요', 'class': 'review-title'}),
        }
        labels = {
            'username' : '아이디',
            'real_name' : '성명',
            'alias_name' : '사용자이름',
            'gender' : '성별',
            'introduce' : '자기소개',
            'is_notify' : '알림여부',
            # 'password' : '비밀번호',
        }

