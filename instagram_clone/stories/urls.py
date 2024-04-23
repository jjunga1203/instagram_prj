from django.contrib import admin
from django.urls import path
from . import views
app_name = 'stories'
urlpatterns = [
    path('create/', views.create, name='create'),
    path('<str:image_name>/', views.get_story_image, name='get_story_image'),
    path('<int:story_id>/', views.detail, name='detail'),
]