from django.contrib import admin
from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('accounts/', views.profile, name='profile'),
    path('', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('upload_img/<int:user_idx>', views.upload_img, name='upload_img'),
    path('profile/<int:user_idx>', views.profile, name='profile'),
]
