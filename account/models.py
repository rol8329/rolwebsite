import uuid6
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userProfile')
    actif=models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def desactivate(self):
        self.actif=False
        self.save()

    def activate(self):
        self.actif=True
        self.save()