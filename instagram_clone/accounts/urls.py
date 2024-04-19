from django.contrib import admin
from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('accounts/', views.profile, name='profile'),
    path('', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]
