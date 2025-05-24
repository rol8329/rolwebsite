from django import forms
from .models import BasePost, ImagePost, VideoPost, AudioPost, FilePost

class BasePostForm(forms.ModelForm):
    class Meta:
        model = BasePost
        fields = ['title', 'content', 'actif']

class ImagePostForm(forms.ModelForm):
    class Meta:
        model = ImagePost
        fields = ['label', 'image']

class VideoPostForm(forms.ModelForm):
    class Meta:
        model = VideoPost
        fields = ['label', 'video']

class AudioPostForm(forms.ModelForm):
    class Meta:
        model = AudioPost
        fields = ['label', 'audio']

class FilePostForm(forms.ModelForm):
    class Meta:
        model = FilePost
        fields = ['label', 'file']
