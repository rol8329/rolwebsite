# account/views.py
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer
)


class RegisterView(APIView):
    """User registration endpoint"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """User login endpoint"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': UserProfileSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProfileView(APIView):
    """User profile endpoint - get and update user profile"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get current user profile"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Update user profile (full update)"""
        serializer = UserProfileSerializer(
            request.user,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'user': serializer.data,
                'message': 'Profile updated successfully'
            }, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request):
        """Update user profile (partial update)"""
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                'user': serializer.data,
                'message': 'Profile updated successfully'
            }, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserListView(APIView):
    """List all users - Owner only"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Check if user is owner
        if request.user.role != 'owner':
            return Response(
                {'error': 'Permission denied. Owner access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        users = User.objects.all()
        serializer = UserProfileSerializer(users, many=True)

        return Response({
            'users': serializer.data,
            'total_count': users.count()
        }, status=status.HTTP_200_OK)


class ChangeUserRoleView(APIView):
    """Change user role - Owner only"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Check if user is owner
        if request.user.role != 'owner':
            return Response(
                {'error': 'Permission denied. Owner access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        user_id = request.data.get('user_id')
        new_role = request.data.get('role')

        # Validate required fields
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not new_role:
            return Response(
                {'error': 'role is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate role
        if new_role not in ['reader', 'creator', 'owner']:
            return Response(
                {'error': 'Invalid role. Must be reader, creator, or owner'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)

            # Prevent self role change to avoid lockout
            if user == request.user and new_role != 'owner':
                return Response(
                    {'error': 'Cannot change your own role from owner'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Remove all existing groups
            user.groups.clear()

            # Add new group
            try:
                group = Group.objects.get(name=new_role)
                user.groups.add(group)
            except Group.DoesNotExist:
                return Response(
                    {'error': f'Role group "{new_role}" does not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({
                'message': f'User role changed to {new_role}',
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Keep the function-based views as they are already simple
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logout user by blacklisting refresh token"""
    try:
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(
            {'message': 'Logout successful'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': 'Invalid token or logout failed'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_permissions_view(request):
    """Get current user's permissions and role info"""
    user = request.user

    return Response({
        'user_id': user.id,
        'email': user.email,
        'role': user.role,
        'permissions_level': user.permissions_level,
        'groups': [group.name for group in user.groups.all()],
        'is_owner': user.role == 'owner',
        'is_creator': user.permissions_level >= 2,
        'can_create_posts': user.permissions_level >= 2,
        'can_manage_users': user.role == 'owner'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def refresh_token_view(request):
    """Manually refresh access token"""
    try:
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        return Response({
            'access': access_token,
            'message': 'Token refreshed successfully'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': 'Invalid refresh token'},
            status=status.HTTP_400_BAD_REQUEST
        )


# Optional: Dashboard data view for different roles
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_data_view(request):
    """Get dashboard data based on user role"""
    user = request.user

    # Base data for all users
    data = {
        'user': UserProfileSerializer(user).data,
        'welcome_message': f'Welcome back, {user.first_name or user.username}!'
    }

    # Role-based data
    if user.role == 'owner':
        # Owner gets full system stats
        data.update({
            'total_users': User.objects.count(),
            'user_roles': {
                'readers': User.objects.filter(groups__name='reader').count(),
                'creators': User.objects.filter(groups__name='creator').count(),
                'owners': User.objects.filter(groups__name='owner').count(),
            },
            'recent_users': UserProfileSerializer(
                User.objects.order_by('-created_at')[:5],
                many=True
            ).data
        })

    elif user.role == 'creator':
        # Creator gets their own stats
        data.update({
            'can_create': True,
            'created_posts_count': 0,  # You can add actual count from blog model
        })

    else:  # reader
        data.update({
            'can_create': False,
            'message': 'You have read-only access'
        })

    return Response(data, status=status.HTTP_200_OK)