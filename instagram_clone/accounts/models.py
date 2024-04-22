from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    gender_choices = (
        ('M', '남성'),
        ('F', '여성'),
        ('O', '선택안함'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    alias_name = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100)
    
    username = models.CharField(max_length=100, unique=True)
    introduce = models.TextField(max_length=100)
    gender = models.CharField(max_length=1, choices=gender_choices, default='O')
    is_notify = models.BooleanField(default = True)
    profile_url = models.CharField(max_length=255, default='')
    
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    profile_url = models.TextField(default='')
    profile_img_name = models.CharField(max_length=100, default='')
