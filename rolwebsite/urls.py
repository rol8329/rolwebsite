#rolwebsite/urls
from django.contrib import admin
from django.urls import path, include
from accueil.views import index

urlpatterns = [
    path("", index, name="index"),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('account-api', include("account.api.urls")),
    path('blog-api', include("blog.api.urls")),
    path('account/', include("account.urls", namespace='account')),
    path('accueil/', include("accueil.urls", namespace='accueil')),
    path('blog/', include("blog.urls", namespace='blog')),
]
