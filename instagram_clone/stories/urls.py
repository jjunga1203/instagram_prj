from django.contrib import admin
from django.urls import path
from . import views
app_name = 'stories'

urlpatterns = [
    path('stories/', views.index, name='index'),
    path('', views.index, name='index'),
]
