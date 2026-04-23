from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models


class CineUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    user_phone = models.CharField(max_length=20, default='', blank=True)

    user_joined_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return (self.user.username)