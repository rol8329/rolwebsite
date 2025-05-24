from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('list/', views.post_list, name='post_list'),                        # Liste des posts
    path('create/', views.post_create, name='post_create'),             # Création d’un post
    path('<uuid:uuid>/update/', views.post_update, name='post_update'),# Modification d’un post
    path('<uuid:uuid>/delete/', views.post_delete, name='post_delete'),# Suppression d’un post
    path('<uuid:uuid>/', views.read_post, name='read_post'),            # Détail d’un post (à ajouter à tes vues)
]
