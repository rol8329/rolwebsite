import uuid6
from django.db import models

class BasePost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ImagePost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    post = models.ForeignKey(BasePost, on_delete=models.CASCADE, related_name='postImagePost')
    label = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.label

class VideoPost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    post = models.ForeignKey(BasePost, on_delete=models.CASCADE, related_name='postVideoPost')
    label = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/')
    def __str__(self):
        return self.label

class AudioPost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    post = models.ForeignKey(BasePost, on_delete=models.CASCADE, related_name='postAudioPost')
    label = models.CharField(max_length=255)
    audio = models.FileField(upload_to='audios/')
    def __str__(self):
        return self.label

class FilePost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    post = models.ForeignKey(BasePost, on_delete=models.CASCADE, related_name='postFilePost')
    label = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    def __str__(self):
        return self.label