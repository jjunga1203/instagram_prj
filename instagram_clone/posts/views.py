from django.shortcuts import render, redirect, get_object_or_404
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

@login_required
def home(request):
    user = get_object_or_404(User, pk=request.user.id)
    followings = user.followings.all()
    
    stories = Story.objects.filter(
        Q(user__in=followings) | Q(user=user), 
        created_at__gte=timezone.now() - timedelta(days=1)
    )

    user_grouped_stories = stories.values('user__id').annotate(num_stories=Count('id'))
    
    posts = Post.objects.filter(
        Q(user__in=followings) | Q(user=user)
    ).order_by("-created_at")
    
    context = {
        'posts': posts,
        'user_grouped_stories': user_grouped_stories,
    }
    return render(request, 'posts/home.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
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
            post.save()
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})

def update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user != post.user:
        return redirect('posts:home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
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
    return redirect('posts:home')

def delete_comment(request, post_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('posts:detail', post_id)

def create_comment_notification(user, post, comment_content):
    message = f'{user.username}님이 회원님의 게시물에 댓글을 남겼습니다: {comment_content}'
    Notification.objects.create(user=post.user, message=message, post=post)

def create_comment(request, pk):
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()

        # 댓글이 작성되었을 때 알림 생성
        create_comment_notification(request.user, post, comment.content)

        return redirect('posts:detail', pk=pk)

    context = {
        'post': post,
        'comment_form': comment_form
    }
    return render(request, 'posts/detail.html', context)

def edit_comment(request, pk):
    # 댓글을 가져옵니다.
    comment = Comment.objects.get(pk=pk)

    # POST 요청을 처리합니다.
    if request.method == 'POST':
        # POST 데이터와 함께 댓글 폼을 초기화합니다.
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            # 폼이 유효하다면 수정된 댓글을 저장합니다.
            comment_form.save()
            # 댓글 수정 후 해당 포스트의 상세 페이지로 리다이렉트합니다.
            return redirect('posts:detail', pk=comment.post.pk)
    else:
        # GET 요청의 경우 초기 댓글 폼을 생성합니다.
        comment_form = CommentForm(instance=comment)

    # 댓글 수정을 위한 폼과 해당 댓글이 속한 포스트를 템플릿 컨텍스트에 추가합니다.
    context = {
        'comment_form': comment_form,
        'post': comment.post
    }
    # 댓글 수정 템플릿을 렌더링합니다.
    return render(request, 'posts/edit_comment.html', context)

def create_like_notification(user, post):
    message = f'{user.username}님이 회원님의 게시물을 좋아합니다.'
    Notification.objects.create(user=post.user, message=message, post=post)

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
