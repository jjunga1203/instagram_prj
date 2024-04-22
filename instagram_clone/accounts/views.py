from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm # , CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm , CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import User
from django.http import JsonResponse


from django.core.files.storage import default_storage
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

# 개인 프로파일 화면
def profile(request, user_idx):
    # print(username)
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    user = User.objects.get(pk=user_idx)
    context = {
        'user':user,
    }

    return render(request, 'accounts/profile.html', context)


# 사진 업로드
def upload_img(request, user_idx):
    # form = UserChangeForm(request.user, request.POST)
    form = get_user_model().objects.get(pk=user_idx)

    if 'profile_img' in request.FILES:
        file = request.FILES['profile_img']
        print(file.name, file)
        
        filename = default_storage.save(file.name, file)
        file_url = default_storage.url(filename)
 
        print(filename, file_url)
        form.profile_url = file_url
        form.save()
    else:
        print("No image file uploaded.")
    
    return redirect('accounts:profile', request.user.id)

       
def signup(request):
    # 이미 로그인한 경우, 회원가입 로직 실행 막기
    if request.user.is_authenticated:
        return redirect('accounts:profile', request.user.id)
    
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    # 이미 로그인한 경우, 정보화면으로 이동
    if request.user.is_authenticated:
        return redirect('accounts:profile', request.user.id)
    
    # 로그인 시도
    # 세션을 생성! 하니까 POST
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            print(request.user.id)
            return redirect('accounts:profile', request.user.id)

    form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/login.html', context)

# logout은 반드시 로그인 상태가 필수조건
@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


# # 이미지 업로드 관련
# def image(request):

#     return render(request, 'sample/index.html')