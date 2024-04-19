from django.contrib import admin
from django.urls import path
from . import views
app_name = 'direct_msgs'

urlpatterns = [
    path('direct_msgs/', views.index, name='index'),
    path('', views.index, name='index'),
]
