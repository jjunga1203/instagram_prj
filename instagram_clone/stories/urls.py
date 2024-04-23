from django.contrib import admin
from django.urls import path
from . import views
app_name = 'stories'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]