from django.urls import path
from .views import VideoPostListView, VideoPostDetailView, AudioPostListView, AudioPostDetailView, ImagePostListView, \
    ImagePostDetailView, FilePostListView, FilePostDetailView, BasePostListView, BasePostDetailView, \
    BasePostGlobalAPIView

urlpatterns = [
    # BasePost CRUD
    path('/posts/', BasePostListView.as_view()),
    path('/posts/global/', BasePostGlobalAPIView.as_view()),
    path('/posts/<uuid:uuid>/', BasePostDetailView.as_view()),

    # ImagePost (Create/Delete/Read)
    path('/posts/<uuid:post_uuid>/images/', ImagePostListView.as_view()),
    path('/images/<uuid:uuid>/', ImagePostDetailView.as_view()),

    # VideoPost
    path('/posts/<uuid:post_uuid>/videos/', VideoPostListView.as_view()),
    path('/videos/<uuid:uuid>/', VideoPostDetailView.as_view()),

    # AudioPost
    path('/posts/<uuid:post_uuid>/audios/', AudioPostListView.as_view()),
    path('/audios/<uuid:uuid>/', AudioPostDetailView.as_view()),

    # FilePost
    path('/posts/<uuid:post_uuid>/files/', FilePostListView.as_view()),
    path('/files/<uuid:uuid>/', FilePostDetailView.as_view()),
]
