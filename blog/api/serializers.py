# serializers.py
from rest_framework import serializers
from blog.models import BasePost, VideoPost, AudioPost, FilePost, ImagePost

class BasePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasePost
        fields = '__all__'

# Individual serializers (for POST operations - exclude uuid and post)
class VideoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPost
        fields = ['label', 'video']

class AudioPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioPost
        fields = ['label', 'audio']

class FilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilePost
        fields = ['label', 'file']

class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['label', 'image']

# Global serializers (for GET operations in global view - include uuid, exclude post)
class VideoPostGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPost
        fields = ['uuid', 'label', 'video']

class AudioPostGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioPost
        fields = ['uuid', 'label', 'audio']

class FilePostGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilePost
        fields = ['uuid', 'label', 'file']

class ImagePostGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['uuid', 'label', 'image']

# Global BasePost serializer
class BasePostGLobalSerializer(serializers.ModelSerializer):
    postImagePost = ImagePostGlobalSerializer(many=True, read_only=True)
    postVideoPost = VideoPostGlobalSerializer(many=True, read_only=True)
    postAudioPost = AudioPostGlobalSerializer(many=True, read_only=True)
    postFilePost = FilePostGlobalSerializer(many=True, read_only=True)

    class Meta:
        model = BasePost
        fields = [
            'uuid',
            'title',
            'content',
            'created_at',
            'updated_at',
            'actif',
            'postImagePost',
            'postVideoPost',
            'postAudioPost',
            'postFilePost'
        ]