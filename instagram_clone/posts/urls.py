from django.contrib import admin
from django.urls import path
from . import views
app_name = 'posts'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('update/<int:pk>', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('<int:post_id>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('create_comment/<int:pk>', views.create_comment, name='create_comment'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('like/<int:post_id>/', views.post_like, name='post_like'),
    path('edit_comment/<int:pk>/', views.edit_comment, name='edit_comment'),
    path('user_posts/', views.user_posts, name='user_posts'),
]

