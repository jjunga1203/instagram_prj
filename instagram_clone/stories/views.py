from django.shortcuts import render, redirect, get_object_or_404
from .models import Story
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.conf import settings
from django.core.files.storage import default_storage

@login_required
def create(request):
    pass


@login_required
def get_story_image(request, image_name):
    # AWS S3 버킷에 저장된 이미지의 URL 가져오기
    image_url = default_storage.url(image_name)
    # 이미지를 클라이언트에 반환
    return redirect(image_url)

@login_required
def detail(request, story_id):
    # 스토리 객체 가져오기
    story = get_object_or_404(Story, id=story_id)
    # 스토리의 자세한 내용을 보여주는 페이지 렌더링
    return render(request, 'stories/story_detail.html', {'story': story})
