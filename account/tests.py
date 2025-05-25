from django.test import TestCase
# test_auth_api.py - Run this after setup to verify everything works
import requests
import json
# test_auth_api.py - Updated for new URL structure
import requests
import json

# Updated BASE_URL to match new structure
BASE_URL = 'http://127.0.0.1:8000/api/account'


def test_registration():
    """Test user registration"""
    print("🔄 Testing user registration...")

    data = {
        'email': 'test@example.com',
        'username': 'testuser',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'testpass123',
        'password_confirm': 'testpass123'
    }

    response = requests.post(f'{BASE_URL}/auth/register/', json=data)

    if response.status_code == 201:
        print("✅ Registration successful!")
        result = response.json()
        print(f"   User: {result['user']['email']}")
        print(f"   Role: {result['user']['role']}")
        return result['access'], result['refresh']
    else:
        print(f"❌ Registration failed: {response.text}")
        return None, None


def test_login():
    """Test user login"""
    print("\n🔄 Testing user login...")

    data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }

    response = requests.post(f'{BASE_URL}/auth/login/', json=data)

    if response.status_code == 200:
        print("✅ Login successful!")
        result = response.json()
        print(f"   User: {result['user']['email']}")
        print(f"   Role: {result['user']['role']}")
        return result['access'], result['refresh']
    else:
        print(f"❌ Login failed: {response.text}")
        return None, None


def test_profile(access_token):
    """Test profile access"""
    print("\n🔄 Testing profile access...")

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{BASE_URL}/profile/', headers=headers)

    if response.status_code == 200:
        print("✅ Profile access successful!")
        result = response.json()
        print(f"   Email: {result['email']}")
        print(f"   Role: {result['role']}")
        print(f"   Permission Level: {result['permissions_level']}")
        return True
    else:
        print(f"❌ Profile access failed: {response.text}")
        return False


def test_permissions(access_token):
    """Test permissions endpoint"""
    print("\n🔄 Testing permissions endpoint...")

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{BASE_URL}/permissions/', headers=headers)

    if response.status_code == 200:
        print("✅ Permissions access successful!")
        result = response.json()
        print(f"   Can create posts: {result['can_create_posts']}")
        print(f"   Can manage users: {result['can_manage_users']}")
        print(f"   Groups: {result['groups']}")
        return True
    else:
        print(f"❌ Permissions access failed: {response.text}")
        return False


def test_dashboard(access_token):
    """Test dashboard endpoint"""
    print("\n🔄 Testing dashboard endpoint...")

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{BASE_URL}/dashboard/', headers=headers)

    if response.status_code == 200:
        print("✅ Dashboard access successful!")
        result = response.json()
        print(f"   Welcome message: {result['welcome_message']}")
        if 'can_create' in result:
            print(f"   Can create: {result['can_create']}")
        return True
    else:
        print(f"❌ Dashboard access failed: {response.text}")
        return False


def test_logout(refresh_token):
    """Test logout"""
    print("\n🔄 Testing logout...")

    data = {'refresh': refresh_token}
    response = requests.post(f'{BASE_URL}/auth/logout/', json=data)

    if response.status_code == 200:
        print("✅ Logout successful!")
        return True
    else:
        print(f"❌ Logout failed: {response.text}")
        return False


def test_all_endpoints():
    """Test all available endpoints"""
    print("\n🔄 Testing all available endpoints...")

    endpoints = [
        ('GET', '/api/account/token/'),
        ('GET', '/api/account/auth/register/'),
        ('GET', '/api/account/auth/login/'),
        ('GET', '/api/account/profile/'),
        ('GET', '/api/account/permissions/'),
        ('GET', '/api/account/dashboard/'),
    ]

    for method, endpoint in endpoints:
        try:
            if method == 'GET':
                response = requests.get(f'http://127.0.0.1:8000{endpoint}')
            print(f"   {method} {endpoint}: Status {response.status_code}")
        except Exception as e:
            print(f"   {method} {endpoint}: Error - {e}")


def main():
    """Run all tests"""
    print("🚀 Starting API Authentication Tests")
    print("=" * 50)

    # Test all endpoints first
    test_all_endpoints()

    # Test registration
    access_token, refresh_token = test_registration()

    if not access_token:
        # If registration fails, try login with existing user
        access_token, refresh_token = test_login()

    if access_token:
        # Test protected endpoints
        test_profile(access_token)
        test_permissions(access_token)
        test_dashboard(access_token)

        # Test logout
        if refresh_token:
            test_logout(refresh_token)

    print("\n" + "=" * 50)
    print("🏁 Tests completed!")


if __name__ == '__main__':
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Make sure Django server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

# FRONTEND CONFIGURATION UPDATE
# Update your React authService.ts base URL:

"""
// src/services/authService.ts
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/account/`,  // Updated to match new structure
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token refresh URL also needs updating:
const response = await axios.post(`${API_BASE_URL}/api/token/refresh/`, {
  refresh: refreshToken,
});
"""

# COMPLETE URL STRUCTURE:
"""
Main Django URLs:
- http://localhost:8000/                    → Homepage
- http://localhost:8000/admin/              → Django Admin
- http://localhost:8000/api/account/        → Account API
- http://localhost:8000/api/blog/           → Blog API

Account API URLs:
- POST /api/account/auth/register/          → Register
- POST /api/account/auth/login/             → Login  
- POST /api/account/auth/logout/            → Logout
- GET  /api/account/profile/                → Get profile
- PUT  /api/account/profile/                → Update profile
- GET  /api/account/permissions/            → Get permissions
- GET  /api/account/dashboard/              → Dashboard data
- GET  /api/account/admin/users/            → List users (Owner only)
- POST /api/account/admin/change-role/      → Change user role (Owner only)

JWT Tokens:
- POST /api/account/token/                  → Get token pair
- POST /api/account/token/refresh/          → Refresh token
"""