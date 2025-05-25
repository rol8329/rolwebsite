# account/api/urls.py (Fixed URL patterns - remove leading slashes)
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from account.api.views import (
    ProtectedView, RegisterView, LoginView, logout_view,
    refresh_token_view, ProfileView, user_permissions_view,
    UserListView, ChangeUserRoleView, dashboard_data_view
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('protected/', ProtectedView.as_view()),

    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/refresh/', refresh_token_view, name='refresh_token'),

    # User profile
    path('profile/', ProfileView.as_view(), name='profile'),
    path('permissions/', user_permissions_view, name='user_permissions'),

    # Admin (Owner only)
    path('admin/users/', UserListView.as_view(), name='user_list'),
    path('admin/change-role/', ChangeUserRoleView.as_view(), name='change_role'),

    # Dashboard
    path('dashboard/', dashboard_data_view, name='dashboard_data'),
]