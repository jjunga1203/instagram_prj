from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.utils.datastructures import MultiValueDictKeyError

@login_required
def image(request):
    if 'image' in request.FILES:
        file = request.FILES['image']
        filename = default_storage.save(file.name, file)
        file_url = default_storage.url(filename)
        print(filename, file_url)
    else:
        print("No image file uploaded.")
    return render(request, 'posts/index.html')
# def image(request):
#     file = request.FILES['image']
#     filename = default_storage.save(file.name, file)
#     file_url = default_storage.url(filename)
#     print(filename , file_url)
#     return render(request, 'sample/index.html')
# Create your views here.

def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/home.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            post = form.save()
            return redirect('posts:detail', post.pk)
    else:
        form = PostForm()
        context = {
            'form': form
        }
        return render(request, 'posts/create.html', context)

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

def create_comment(request, pk):
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        return redirect('posts:detail', pk)
    context = {
        'post': post,
        'comment_form': comment_form
    }
    return render(request, 'posts/detail.html', context)

def post_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    # 이미 좋아요를 한 사람의 경우에는 좋아요를 취소
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user, through_defaults={'memo': '메모'})
    return redirect('posts:home')
