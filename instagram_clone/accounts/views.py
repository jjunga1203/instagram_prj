from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm # , CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import User
from django.db.models import Q 
def search(request):
    searched_users = None
    user_id = request.GET.get('user_id')
    if user_id:
        # Search for users whose alias_name or real_name matches the user_id
        searched_users = User.objects.filter(
            Q(alias_name__icontains=user_id) | Q(real_name__icontains=user_id)
        )
    return render(request, 'accounts/search.html', {'searched_users': searched_users})


from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm # , CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import User
from django.http import JsonResponse


# Create your views here.
def profile(request, username):
    user = get_user_model().objects.get(username=username)
    context = {
        'user': user
    }
    return render(request, 'accounts/profile.html', context)

def signup(request):
    # 이미 로그인한 경우, 회원가입 로직 실행 막기
    # if request.user.is_authenticated:
    #     return redirect('accounts:index', request.user.id)
    
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
        return redirect('accounts:index', request.user.id)
    
    # 로그인 시도
    # 세션을 생성! 하니까 POST
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            print(request.user.id)
            return redirect('accountscd:profile', request.user.id)

    form = AuthenticationForm()
    context = {
        'form':form
    }
    return render(request, 'accounts/login.html', context)

def search(request):
    searched_users = None
    user_id = request.GET.get('user_id')
    if user_id:
        # Search for users whose alias_name or real_name matches the user_id
        searched_users = User.objects.filter(
            Q(alias_name__icontains=user_id) | Q(real_name__icontains=user_id)
        )
    return render(request, 'accounts/search.html', {'searched_users': searched_users})

def follow(request, user_id):
    user = get_user_model().objects.get(pk=user_id)
    if request.user == user:
        return redirect('accounts:profile', user.username)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.follower.add(request.user)
    return redirect('accounts:profile', user.username)