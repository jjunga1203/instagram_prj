from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Post, Comment
from accounts.models import User
from stories.models import Story
from notifications.models import Notification
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

@login_required
def home(request):
    user = get_object_or_404(User, pk=request.user.id)
    
    # 현재 로그인한 사용자가 팔로우한 사용자들의 목록
    followings = user.followings.all()

    # 필터링 조건
    filter_condition = (
        Q(user__in=followings) | Q(user=user)
    ) & Q(created_at__gte=timezone.now() - timedelta(days=1))

    # 필터링된 결과를 사용하여 그루핑 및 어노테이션 적용
    user_grouped_stories = (
        Story.objects
        .filter(filter_condition)
        .values('user__id', 'user__username', 'user__profile_url', 'user__alias_name')
        .annotate(num_stories=Count('id'))
    )
    
    # 포스트들을 가져오고, 시간을 계산하여 context에 추가
    posts = Post.objects.filter(
        Q(user__in=followings) | Q(user=user)
    ).order_by("-created_at")

    # 시간 변수를 미리 정의
    time_since_created = ""

    for post in posts:
        # 현재 시간과 포스트 작성 시간의 차이를 계산
        time_difference = timezone.now() - post.created_at
        if time_difference < timedelta(minutes=1):
            seconds_since_created = int(time_difference.total_seconds())
            time_since_created = f"{seconds_since_created}초 전"
        elif time_difference < timedelta(hours=1):
            minutes_since_created = int(time_difference.total_seconds() // 60)
            time_since_created = f"{minutes_since_created}분 전"
        elif time_difference < timedelta(days=1):
            hours_since_created = int(time_difference.total_seconds() // 3600)
            time_since_created = f"{hours_since_created}시간 전"
        else:
            days_since_created = int(time_difference.total_seconds() // 86400)
            time_since_created = f"{days_since_created}일 전"

    context = {
        'user': user,
        'posts': posts,
        'user_grouped_stories': user_grouped_stories,
        'time_since_created': time_since_created
    }
    return render(request, 'posts/home.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # 이미지를 S3에 업로드
            if 'image' in request.FILES:
                image = request.FILES['image']
                filename = default_storage.save(image.name, image)
                image_url = default_storage.url(filename)
            else:
                image_url = None

            # 이미지를 S3에 업로드
            if 'image' in request.FILES:
                image = request.FILES['image']
                filename = default_storage.save(image.name, image)
                image_url = default_storage.url(filename)
            else:
                image_url = None

            post = form.save(commit=False)
            post.user = request.user
            post.image = image_url  # 이미지 URL을 모델에 저장
            post.image = image_url  # 이미지 URL을 모델에 저장
            post.save()
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})

@login_required
def update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user != post.user:
        return redirect('posts:home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)  # request.FILES 추가
        form = PostForm(request.POST, request.FILES, instance=post)  # request.FILES 추가
        if form.is_valid():
            # 이미지를 S3에 업로드
            if 'image' in request.FILES:
                image = request.FILES['image']
                filename = default_storage.save(image.name, image)
                image_url = default_storage.url(filename)
                post.image = image_url  # 이미지 URL을 모델에 저장

            # 이미지를 S3에 업로드
            if 'image' in request.FILES:
                image = request.FILES['image']
                filename = default_storage.save(image.name, image)
                image_url = default_storage.url(filename)
                post.image = image_url  # 이미지 URL을 모델에 저장

            form.save()
            return redirect('posts:detail', post.pk)
        
        
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'posts/update.html', context)

def detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'posts/detail.html', context)

def delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.user:
        post.delete()

    
    # 바로 인덱스 페이지로 리다이렉트합니다.
    return redirect(reverse('accounts:index', kwargs={'user_idx': request.user.id}))
    
    # 바로 인덱스 페이지로 리다이렉트합니다.
    return redirect(reverse('accounts:index', kwargs={'user_idx': request.user.id}))

from django.shortcuts import redirect, HttpResponse
from django.contrib import messages

def delete_comment(request, post_id, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        if request.user == comment.user:
            comment.delete()
            return redirect('posts:detail', post_id)
        else:
            # Display an error message if the user is not the owner of the comment
            messages.error(request, "You don't have permission to delete this comment.")
            return redirect('posts:detail', post_id)
    except Comment.DoesNotExist:
        # Display an error message if the comment does not exist
        messages.error(request, "The comment you're trying to delete does not exist.")
        return redirect('posts:detail', post_id)


def create_comment_notification(user, post, comment_content):
    message = f'{user.real_name}님이 회원님의 게시물에 댓글을 남겼습니다: {comment_content}'
    Notification.objects.create(user=post.user, message=message, post=post, msg_user_id=user.id, msg_user_real_name=user.real_name)


def create_comment(request, pk):
    referring_url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post = Post.objects.get(pk=pk)
            comment = Comment.objects.create(post=post, user=request.user, content=content)

            # 댓글이 작성되었을 때 알림 생성
            create_comment_notification(request.user, post, content)


    return HttpResponseRedirect(referring_url) if referring_url else redirect('posts:home')


@require_POST
def edit_comment(request, pk):
    referring_url = request.META.get('HTTP_REFERER')
    comment = Comment.objects.get(pk=pk)
    form = CommentForm(request.POST, instance=comment)
    
    if form.is_valid():
        form.save()

    return HttpResponseRedirect(referring_url) if referring_url else redirect('posts:home')

        

def create_like_notification(user, post):
    message = f'{user.real_name}님이 회원님의 게시물을 좋아합니다.'
    # Notification.objects.create(user=post.user, message=message, post=post)
    Notification.objects.create(user=post.user, message=message, post=post, msg_user_id=user.id, msg_user_real_name=user.real_name)

def post_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    # 이미 좋아요를 한 사람의 경우에는 좋아요를 취소
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user, through_defaults={'memo': '메모'})
        # 좋아요 알림 생성
        create_like_notification(request.user, post)
    return redirect('posts:home')

def user_posts(request):
    # 현재 사용자가 작성한 모든 글을 가져옴
    user_posts = Post.objects.filter(user=request.user)
    return render(request, 'posts/user_posts.html', {'user_posts': user_posts})
