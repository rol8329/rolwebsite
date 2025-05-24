#account/api/urls
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.api.views import ProtectedView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('protected/', ProtectedView.as_view()),
]