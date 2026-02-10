from django.db import models
from django.contrib.auth.models import AbstractUser
import string
import random
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    username = models.CharField(max_length=300, default='username')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

def generateShortCode():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class urlShort(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    original_url = models.URLField(max_length=10000)
    short = models.CharField(max_length=10, default='short url', unique=True)
    click = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.original_url} -- ({self.created_at})"
    
    
    