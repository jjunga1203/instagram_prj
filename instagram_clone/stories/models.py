from django.db import models
from accounts.models import User
from django.utils import timezone

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories/')
    created_at = models.DateTimeField(default=timezone.now)