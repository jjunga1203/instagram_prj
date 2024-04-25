from django.contrib import admin
from django.urls import path
from . import views
app_name = 'stories'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('archive/', views.archive, name='archive'),
]