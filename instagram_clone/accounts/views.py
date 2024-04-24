from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView

from .models import User
from notifications.models import Notification
from posts.models import Post
from django.db.models import Q 

from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse

from django.core.files.storage import default_storage
from django.utils.datastructures import MultiValueDictKeyError

from django.contrib.auth.hashers import check_password


# Create your views here.
@login_required
def change_pw(request, user_idx):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    # fcuser = Fcuser.objects.get(username=username)
    # if not check_password(password, Fcuser.username):
    #     self.add_error('password', '비밀번호가 틀렸습니다.')

    my_p = PasswordChangeForm(request.user,request.POST)
    print(request.POST['password'])
    if request.POST['password'] == my_p.password:
        my_p.password = request.POST['password1']
        my_p.save()

        update_session_auth_hash(request, my_p)
        return redirect('accounts:profile', request.user.id)
    else:
        return redirect('accounts:profile', request.user.id)

@login_required
def index(request, user_idx):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user = User.objects.get(pk=user_idx)
    # 사용자가 작성한 게시글 가져오기
    user_posts = Post.objects.filter(user=user)
        
    # 팔로잉 및 팔로워 수 계산
    following_count = user.followings.count() 
    follower_count = user.followers.count()   

    context = {
        'user': user,
        'following_count': following_count,
        'follower_count': follower_count,
        'user_posts': user_posts,  # 사용자가 작성한 게시글을 컨텍스트에 추가

    } 

    return render(request, 'accounts/index.html', context)


import json
from django.http import JsonResponse

# 개인 프로파일 화면 (편집모드로 띄우기)
@login_required
def profile(request, user_idx):
    # 사용자가 로그인되어 있는지 확인
    if not request.user.is_authenticated:
        return redirect('accounts:login')
  
    # 사용자 정보 가져오기
    user = User.objects.get(pk=user_idx)
    print(user.id, user.pk)

    if request.method == 'POST':
        data = json.loads(request.body)

        # JSON 데이터에서 'gender' 필드 값을 가져옵니다.
        gender = data.get('gender')
        introduce = data.get('introduce')

        print(gender, introduce)
        form = CustomUserChangeForm(data, instance=user)
        print(form.username)
        if form.is_valid():
            print(form.username)
            form.introduce = introduce
            form.gender = gender

            form.save()
        else:
            print('저장오류')
        return redirect('accounts:profile', request.user.id)
    else:
        print(request.user)
        
        # user = CustomUserChangeForm(instance=user)
    context = {
        'user': user,
    }

    return render(request, 'accounts/profile.html', context) 


# 개인 프로파일 화면 (편집모드로 띄우기)
def old_profile(request, user_idx):
    # 사용자 정보 가져오기
    user = User.objects.get(pk=user_idx)
    # 사용자가 작성한 게시글 가져오기
    user_posts = Post.objects.filter(user=user)
    # 팔로잉 및 팔로워 수 계산
    following_count = user.followings.count() 
    follower_count = user.followers.count()   

    # 사용자가 로그인되어 있는지 확인
    if not request.user.is_authenticated:
        return redirect('accounts:login')
  

    context = {
        'user': user,
        'following_count': following_count,
        'follower_count': follower_count,
        'user_posts': user_posts,  # 사용자가 작성한 게시글을 컨텍스트에 추가

    } 


    return render(request, 'accounts/profile.html', context) 


# 사진 업로드
@login_required
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

    return redirect('accounts:profile', request.user.id)

@login_required
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
        print(request)

        if form.is_valid():
            form.save()
 
            return redirect('accounts:login')
        else:
            print(form.errors)
            return redirect('accounts:signup')
    else:
        form = CustomUserCreationForm()
        context = {
            'form':form
        }
    return render(request, 'accounts/signup.html', context)


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm


def login(request):
    # 이미 로그인한 경우, 정보화면으로 이동
    if request.user.is_authenticated:
        return redirect('accounts:index', request.user.id)
    
    # 로그인 시도
    # 세션을 생성! 하니까 POST
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            print(request.user.id)
            return redirect('accounts:index', request.user.id)

    form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/login.html', context)

@login_required
def search(request):
    searched_users = None
    searched_posts = None
    search_keyword = request.GET.get('search_keyword')
    
    if search_keyword:
        if search_keyword.startswith('#'):  # 해시태그인 경우
            searched_posts = Post.objects.filter(
                content__icontains=search_keyword
                ).order_by("-created_at")

        else:  # 해시태그가 아닌 경우 유저를 검색
            searched_users = User.objects.filter(
                Q(alias_name__icontains=search_keyword) | 
                Q(real_name__icontains=search_keyword) |
                Q(username__icontains=search_keyword)
            )
            
    context = {
        'searched_users': searched_users, 
        'searched_posts': searched_posts
    } 
    
    return render(request, 'accounts/search.html', context)

def create_newfollower_notification(user, followed_user):
    # message = f'{user.username}님이 회원님을 팔로우하기 시작했습니다.'
    message = f'님이 회원님을 팔로우하기 시작했습니다.'
    Notification.objects.create(user=followed_user, message=message, msg_user_id=user.id, msg_user_real_name=user.real_name)

@login_required
def follow(request, user_idx):
    user = request.user
    followed_user = User.objects.get(pk=user_idx)
    
    if user in followed_user.followers.all():
        followed_user.followers.remove(user)
    else:
        followed_user.followers.add(user)
        # 새로운 팔로워가 생겼을 때 알림 생성
        create_newfollower_notification(user, followed_user)
        
    return redirect('accounts:index', user_idx=user_idx)


# logout은 반드시 로그인 상태가 필수조건
@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


# # 이미지 업로드 관련
# def image(request):

#     return render(request, 'sample/index.html')