from django.contrib import admin
from blog.models import BasePost, ImagePost, VideoPost, AudioPost, FilePost

# Register your models here.
admin.site.register(BasePost)
admin.site.register(ImagePost)
admin.site.register(VideoPost)
admin.site.register(AudioPost)
admin.site.register(FilePost)
