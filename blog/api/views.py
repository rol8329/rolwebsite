from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.api.serializers import BasePostSerializer, VideoPostSerializer, AudioPostSerializer, ImagePostSerializer, \
    FilePostSerializer, BasePostGLobalSerializer
from blog.models import BasePost, VideoPost, AudioPost, ImagePost, FilePost


# Views
class BasePostListView(APIView):
    """
    Handles GET (list) and POST (create) for BasePost.
    """

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        posts = BasePost.objects.filter(actif=True).order_by('-created_at')
        serializer = BasePostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print("REQUEST DATA", request.data)
        serializer = BasePostSerializer(data=request.data)
        print("STEP 1")
        if serializer.is_valid():
            print("STEP 2")
            serializer.save()
            print("STEP 3")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasePostDetailView(APIView):
    """
    Handles GET (retrieve), PUT (update), PATCH (partial update), and DELETE (delete) for BasePost.
    """
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, uuid):
        post = get_object_or_404(BasePost, uuid=uuid)
        serializer = BasePostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        post = get_object_or_404(BasePost, uuid=uuid)
        serializer = BasePostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, uuid):
        post = get_object_or_404(BasePost, uuid=uuid)
        serializer = BasePostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        post = get_object_or_404(BasePost, uuid=uuid)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VideoPostListView(APIView):
    """
    Handles GET (list) and POST (create) for VideoPost based on a given BasePost.
    """
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, post_uuid):
        video_posts = VideoPost.objects.filter(post__uuid=post_uuid)
        serializer = VideoPostSerializer(video_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_uuid):
        # Get the BasePost instance
        base_post = get_object_or_404(BasePost, uuid=post_uuid)

        serializer = VideoPostSerializer(data=request.data)
        if serializer.is_valid():
            # Save with the post relationship
            serializer.save(post=base_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoPostDetailView(APIView):
    """
    Handles GET (retrieve), PUT (update), PATCH (partial update), DELETE (delete), and DOWNLOAD for VideoPost.
    """
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, uuid):
        video_post = get_object_or_404(VideoPost, uuid=uuid)
        serializer = VideoPostSerializer(video_post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        video_post = get_object_or_404(VideoPost, uuid=uuid)
        serializer = VideoPostSerializer(video_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, uuid):
        video_post = get_object_or_404(VideoPost, uuid=uuid)
        serializer = VideoPostSerializer(video_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        video_post = get_object_or_404(VideoPost, uuid=uuid)
        video_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, uuid, format=None):
        video_post = get_object_or_404(VideoPost, uuid=uuid)
        response = FileResponse(video_post.video.open(), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{video_post.label}.mp4"'
        return response

class AudioPostListView(APIView):
    """
    Handles GET (list) and POST (create) for AudioPost based on a given BasePost.
    """
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, post_uuid):
        audio_posts = AudioPost.objects.filter(post__uuid=post_uuid)
        serializer = AudioPostSerializer(audio_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_uuid):
        # Get the BasePost instance
        base_post = get_object_or_404(BasePost, uuid=post_uuid)

        serializer = AudioPostSerializer(data=request.data)
        if serializer.is_valid():
            # Save with the post relationship
            serializer.save(post=base_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AudioPostDetailView(APIView):
    """
    Handles GET (retrieve), PUT (update), PATCH (partial update), DELETE (delete), and DOWNLOAD for AudioPost.
    """
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, uuid):
        audio_post = get_object_or_404(AudioPost, uuid=uuid)
        serializer = AudioPostSerializer(audio_post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        audio_post = get_object_or_404(AudioPost, uuid=uuid)
        serializer = AudioPostSerializer(audio_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, uuid):
        audio_post = get_object_or_404(AudioPost, uuid=uuid)
        serializer = AudioPostSerializer(audio_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        audio_post = get_object_or_404(AudioPost, uuid=uuid)
        audio_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, uuid, format=None):
        audio_post = get_object_or_404(AudioPost, uuid=uuid)
        response = FileResponse(audio_post.audio.open(), content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename="{audio_post.label}.mp3"'
        return response

class ImagePostListView(APIView):
    """
    Handles GET (list) and POST (create) for ImagePost based on a given BasePost.
    """
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, post_uuid):
        image_posts = ImagePost.objects.filter(post__uuid=post_uuid)
        serializer = ImagePostSerializer(image_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_uuid):
        print("REQUEST DATA", request.data)

        # Get the BasePost instance
        base_post = get_object_or_404(BasePost, uuid=post_uuid)
        print("BLOG POST", base_post)

        serializer = ImagePostSerializer(data=request.data)
        print("STEP 2")
        if serializer.is_valid():
            print("STEP 3")
            # Save with the post relationship
            serializer.save(post=base_post)
            print("STEP 4")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImagePostDetailView(APIView):
    """
    Handles GET (retrieve), PUT (update), PATCH (partial update), DELETE (delete), and DOWNLOAD for ImagePost.
    """
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, uuid):
        image_post = get_object_or_404(ImagePost, uuid=uuid)
        serializer = ImagePostSerializer(image_post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        image_post = get_object_or_404(ImagePost, uuid=uuid)
        serializer = ImagePostSerializer(image_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, uuid):
        image_post = get_object_or_404(ImagePost, uuid=uuid)
        serializer = ImagePostSerializer(image_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        image_post = get_object_or_404(ImagePost, uuid=uuid)
        image_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, uuid, format=None):
        image_post = get_object_or_404(ImagePost, uuid=uuid)
        response = FileResponse(image_post.image.open(), content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename="{image_post.label}.jpg"'
        return response

class FilePostListView(APIView):
    """
    Handles GET (list) and POST (create) for FilePost based on a given BasePost.
    """
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, post_uuid):
        file_posts = FilePost.objects.filter(post__uuid=post_uuid)
        serializer = FilePostSerializer(file_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_uuid):
        # Get the BasePost instance
        base_post = get_object_or_404(BasePost, uuid=post_uuid)

        serializer = FilePostSerializer(data=request.data)
        if serializer.is_valid():
            # Save with the post relationship
            serializer.save(post=base_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilePostDetailView(APIView):
    """
    Handles GET (retrieve), PUT (update), PATCH (partial update), DELETE (delete), and DOWNLOAD for FilePost.
    """
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, uuid):
        file_post = get_object_or_404(FilePost, uuid=uuid)
        serializer = FilePostSerializer(file_post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        file_post = get_object_or_404(FilePost, uuid=uuid)
        serializer = FilePostSerializer(file_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, uuid):
        file_post = get_object_or_404(FilePost, uuid=uuid)
        serializer = FilePostSerializer(file_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        file_post = get_object_or_404(FilePost, uuid=uuid)
        file_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, uuid, format=None):
        file_post = get_object_or_404(FilePost, uuid=uuid)
        response = FileResponse(file_post.file.open(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_post.label}"'
        return response


class BasePostGlobalAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        """
        Get all active BasePosts with their related Image, Video, Audio, and File posts.
        Optimized with prefetch_related to avoid N+1 queries.
        """
        posts = BasePost.objects.filter(actif=True).prefetch_related(
            'postImagePost',
            'postVideoPost',
            'postAudioPost',
            'postFilePost'
        ).order_by('-created_at')

        serializer = BasePostGLobalSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)