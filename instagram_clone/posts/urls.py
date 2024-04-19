from django.contrib import admin
from django.urls import path
from . import views
app_name = 'posts'

urlpatterns = [
    path('posts/', views.home, name='home'),
    path('', views.home, name='home'),
]
