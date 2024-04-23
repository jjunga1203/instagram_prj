from django.contrib import admin
from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('accounts/', views.profile, name='profile'),
    path('index/<int:user_idx>', views.index, name='index'),
    path('', views.profile, name='profile'),
    
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('upload_img/<int:user_idx>', views.upload_img, name='upload_img'),
    path('delete_img/<int:user_idx>', views.delete_img, name='delete_img'),
    path('profile/<int:user_idx>', views.profile, name='profile'),
    path('change_pw/<int:user_idx>', views.change_pw, name='change_pw'),
   
    path('search/', views.search, name='search'),
    path('follow/<int:user_idx>', views.follow, name='follow'),
]