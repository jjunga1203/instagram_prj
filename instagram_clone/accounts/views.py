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

from django.http import JsonResponse

# Create your views here.
def change_pw(request, user_idx):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    my_p = User.objects.get(id=user_idx)
    if request.POST['cur_pw'] == my_p.password:
        my_p.password = request.POST['password1']
        my_p.save()

        update_session_auth_hash(request, my_p)
        return redirect('accounts:profile', request.user.id)
    else:
        return redirect('accounts:profile', request.user.id)


def index(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user = User.objects.get(pk=request.user.id)
    context = {
        'user':user,
    }

    return render(request, 'accounts/index.html', context)
            
# 개인 프로파일 화면
def profile(request, user_idx):
    # print(username)
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    # user = CustomUserChangeForm(request.user, request.POST)

    if request.method == 'post':
        user = User.objects.get(pk=user_idx)
        context = {
            'user':user,
        }

        return render(request, 'accounts/profile.html', context)
    else:
        user = User.objects.get(pk=user_idx)
        # user = CustomUserChangeForm(instance=request.user)
        # print(user.id)
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
        form.profile_img_name = filename
        form.save()
    else:
        print("No image file uploaded.")
    
    # context = {
    #     'profile_url': file_url,
    #     'profile_img_name' : filename,
    # }
    # return JsonResponse(context)

    return redirect('accounts:profile', request.user.id)

def delete_img(request, user_idx):
    form = get_user_model().objects.get(pk=user_idx)
    default_storage.delete(form.profile_img_name)

    form.profile_url = ''
    form.profile_img_name = ''
    form.save()
    print('profile_img delete...')

    # 팔로우 성공을 JSON 형태로 반환
    context = {
        'profile_url': form.profile_url,
    }
    
    return redirect('accounts:profile', request.user.id)

    # return JsonResponse(context)

def signup(request):
    # 이미 로그인한 경우, 회원가입 로직 실행 막기
    if request.user.is_authenticated:
        return redirect('accounts:profile', request.user.id)
    
    if request.method == 'POST':
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