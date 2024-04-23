from django.shortcuts import render, redirect, get_object_or_404
from .models import Story
from .forms import StoryForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.conf import settings
from django.core.files.storage import default_storage
from django.utils import timezone

@login_required
def create(request):
    print(request.method)
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user 
            story.save()
            
            # 파일을 S3에 업로드
            file = request.FILES['image']
            filename = default_storage.save(file.name, file)
            file_url = default_storage.url(filename)
            print(filename, file_url)
            
            return redirect('stories:detail', pk=story.pk)  # 상세 페이지로 리디렉션
        else:
            print(form.errors)
    else:
        form = StoryForm()
    return render(request, 'stories/create.html', {'form': form})

@login_required
def detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    return render(request, 'stories/detail.html', {'story': story})

@login_required
def delete(request, pk):
    story = get_object_or_404(Story, pk=pk)
    story.is_expired = True
    story.save()
    return redirect('post:home')

@login_required
def archive(request):
    user = request.user
    archived_stories = Story.objects.filter(created_at__lte=timezone.now() - timezone.timedelta(days=1), user=user)
    return render(request, 'stories/archive.html', {'archived_stories': archived_stories})