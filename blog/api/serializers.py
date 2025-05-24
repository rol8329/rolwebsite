from rest_framework import serializers
from blog.models import BasePost, VideoPost, AudioPost, FilePost, ImagePost


class BasePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasePost
        fields = '__all__'

class VideoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPost
        fields = '__all__'

class AudioPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioPost
        fields = '__all__'

class FilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilePost
        fields = '__all__'


class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = '__all__'

class BasePostGLobalSerializer(serializers.ModelSerializer):
    postImagePost = ImagePostSerializer(many=True, read_only=True)
    postVideoPost = VideoPostSerializer(many=True, read_only=True)
    postAudioPost = AudioPostSerializer(many=True, read_only=True)
    postFilePost = FilePostSerializer(many=True, read_only=True)

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