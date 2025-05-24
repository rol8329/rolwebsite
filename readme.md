# Django Backend - Blog Dashboard API

A robust Django REST Framework backend for a multi-media blogging platform. Provides comprehensive API endpoints for blog post management, media handling, and user authentication.

## 🏗️ Architecture Overview

### Core Components
- **Django 5.2**: Web framework
- **Django REST Framework**: API development
- **JWT Authentication**: Token-based security
- **SQLite**: Development database (PostgreSQL ready)
- **Media Handling**: File upload and serving
- **CORS Support**: Cross-origin requests

### App Structure
```
backend/
├── rolwebsite/           # Main project settings
│   ├── settings.py       # Configuration
│   ├── urls.py          # Root URL routing
│   └── wsgi.py          # WSGI application
├── blog/                # Blog application
│   ├── models.py        # Data models
│   ├── api/
│   │   ├── serializers.py # DRF serializers
│   │   ├── views.py      # API views
│   │   └── urls.py       # API routing
│   ├── migrations/       # Database migrations
│   └── admin.py         # Django admin
├── account/             # User authentication
├── media/               # Uploaded files
└── requirements.txt     # Dependencies
```

## 📊 Data Models

### BasePost Model
Core blog post entity with UUID primary key and timestamps.

```python
class BasePost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)
```

### Media Models
Each media type has its own model linked to BasePost via ForeignKey.

```python
class ImagePost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    post = models.ForeignKey(BasePost, on_delete=models.CASCADE, related_name='postImagePost')
    label = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')

class VideoPost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    post = models.ForeignKey(BasePost, on_delete=models.CASCADE, related_name='postVideoPost')
    label = models.CharField(max_length=255)
    video = models.FileField(upload_to='videos/')

class AudioPost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    post = models.ForeignKey(BasePost, on_delete=models.CASCADE, related_name='postAudioPost')
    label = models.CharField(max_length=255)
    audio = models.FileField(upload_to='audios/')

class FilePost(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)
    post = models.ForeignKey(BasePost, on_delete=models.CASCADE, related_name='postFilePost')
    label = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
```

### Key Design Decisions
- **UUID6 Primary Keys**: Better performance and security than auto-incrementing IDs
- **Related Names**: Descriptive reverse relationships for easy querying
- **Separate Media Models**: Flexible schema allowing multiple files per post
- **File Organization**: Automatic directory structure for different media types

## 🛠️ API Endpoints

### Base Posts
| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/blog-api/posts/` | List all active posts | Optional |
| POST | `/blog-api/posts/` | Create new post | Required |
| GET | `/blog-api/posts/{uuid}/` | Get specific post | Optional |
| PUT | `/blog-api/posts/{uuid}/` | Update entire post | Required |
| PATCH | `/blog-api/posts/{uuid}/` | Partial update | Required |
| DELETE | `/blog-api/posts/{uuid}/` | Delete post | Required |

### Global Posts (with Media)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/blog-api/posts/global/` | Posts with all related media |

### Media Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/blog-api/posts/{uuid}/images/` | List/create images for post |
| GET/POST | `/blog-api/posts/{uuid}/videos/` | List/create videos for post |
| GET/POST | `/blog-api/posts/{uuid}/audios/` | List/create audio for post |
| GET/POST | `/blog-api/posts/{uuid}/files/` | List/create files for post |

### Individual Media
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/PUT/PATCH/DELETE | `/blog-api/images/{uuid}/` | Image operations |
| GET/PUT/PATCH/DELETE | `/blog-api/videos/{uuid}/` | Video operations |
| GET/PUT/PATCH/DELETE | `/blog-api/audios/{uuid}/` | Audio operations |
| GET/PUT/PATCH/DELETE | `/blog-api/files/{uuid}/` | File operations |

## 🔐 Authentication & Permissions

### JWT Token Authentication
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### Permission Classes
- **AllowAny()**: GET requests on posts and media
- **IsAuthenticated()**: POST, PUT, PATCH, DELETE operations

### Usage
```bash
# Get access token
curl -X POST http://127.0.0.1:8000/account-api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'

# Use token in requests
curl -X POST http://127.0.0.1:8000/blog-api/posts/ \
  -H "Authorization: Bearer your_access_token" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Post","content":"Post content"}'
```

## 📁 File Upload & Media Handling

### Configuration
```python
# Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# File upload limits
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Supported file types
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
ALLOWED_VIDEO_TYPES = ['video/mp4', 'video/webm', 'video/avi']
ALLOWED_AUDIO_TYPES = ['audio/mp3', 'audio/wav', 'audio/ogg']
```

### Media Directory Structure
```
media/
├── images/           # ImagePost uploads
├── videos/           # VideoPost uploads
├── audios/           # AudioPost uploads
└── files/            # FilePost uploads
```

### Upload Example
```bash
# Upload image to post
curl -X POST http://127.0.0.1:8000/blog-api/posts/{post_uuid}/images/ \
  -H "Authorization: Bearer your_token" \
  -F "label=My Image" \
  -F "image=@/path/to/image.jpg"
```

## 🗄️ Database Schema

### Relationships
```
BasePost (1) ←→ (Many) ImagePost
BasePost (1) ←→ (Many) VideoPost  
BasePost (1) ←→ (Many) AudioPost
BasePost (1) ←→ (Many) FilePost
```

### Key Constraints
- **Cascade Deletion**: Deleting a BasePost removes all related media
- **UUID Primary Keys**: All models use UUID6 for unique identification
- **File Path Storage**: Media files stored with relative paths
- **Timestamp Tracking**: Automatic created_at and updated_at fields

## 🚀 Setup Instructions

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install django==5.2
pip install djangorestframework
pip install django-cors-headers
pip install djangorestframework-simplejwt
pip install uuid6
pip install Pillow  # For ImageField support
```

### 2. Django Configuration
```bash
# Create Django project (if starting fresh)
django-admin startproject rolwebsite
cd rolwebsite

# Create blog app
python manage.py startapp blog
python manage.py startapp account
```

### 3. Settings Configuration
Update `settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'blog',
    'account',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... other middleware
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### 4. Database Setup
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### 5. Run Development Server
```bash
python manage.py runserver
```

## 🔧 API Serializers

### Global Serializer (with Prefetch Optimization)
```python
class BasePostGLobalSerializer(serializers.ModelSerializer):
    postImagePost = ImagePostGlobalSerializer(many=True, read_only=True)
    postVideoPost = VideoPostGlobalSerializer(many=True, read_only=True)
    postAudioPost = AudioPostGlobalSerializer(many=True, read_only=True)
    postFilePost = FilePostGlobalSerializer(many=True, read_only=True)

    class Meta:
        model = BasePost
        fields = [
            'uuid', 'title', 'content', 'created_at', 'updated_at', 'actif',
            'postImagePost', 'postVideoPost', 'postAudioPost', 'postFilePost'
        ]
```

### Media Serializers
```python
# For creation (excludes uuid and post)
class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['label', 'image']

# For global views (includes uuid, excludes post)
class ImagePostGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['uuid', 'label', 'image']
```

## 🔍 Performance Optimizations

### Query Optimization
```python
# Efficient global posts retrieval
posts = BasePost.objects.filter(actif=True).prefetch_related(
    'postImagePost',
    'postVideoPost', 
    'postAudioPost',
    'postFilePost'
).order_by('-created_at')
```

### Caching Strategy
- **Browser Caching**: Static and media files cached with headers
- **Database Indexing**: UUID fields automatically indexed
- **Query Prefetching**: Related media loaded in single query

## 🧪 Testing

### API Testing with curl
```bash
# Test post creation
curl -X POST http://127.0.0.1:8000/blog-api/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Post","content":"Test content","actif":true}'

# Test global posts endpoint
curl http://127.0.0.1:8000/blog-api/posts/global/

# Test media upload
curl -X POST http://127.0.0.1:8000/blog-api/posts/{uuid}/images/ \
  -F "label=Test Image" \
  -F "image=@test.jpg"
```

### Django Admin
Access admin interface at `http://127.0.0.1:8000/admin/` to:
- View and edit posts
- Manage media files
- Monitor user activity
- Test data relationships

## 🚨 Security Considerations

### File Upload Security
- **File Type Validation**: Restricted to specific MIME types
- **File Size Limits**: Configurable upload size restrictions
- **Path Sanitization**: Secure file path generation
- **Virus Scanning**: Consider adding for production

### API Security
- **JWT Expiration**: Short-lived access tokens
- **CORS Configuration**: Restricted origins
- **Rate Limiting**: Consider adding django-ratelimit
- **Input Validation**: DRF serializer validation

## 🌐 Production Deployment

### Environment Variables
```bash
# .env file
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### Database Migration
```bash
# Switch to PostgreSQL
pip install psycopg2-binary

# Update DATABASES in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files & Media
```python
# Production settings
STATIC_ROOT = '/path/to/static/'
MEDIA_ROOT = '/path/to/media/'

# Use cloud storage for media files
# AWS S3, Google Cloud Storage, etc.
```

## 📝 API Documentation

### Response Formats
```json
// BasePost Response
{
  "uuid": "01234567-89ab-cdef-0123-456789abcdef",
  "title": "My Blog Post",
  "content": "Post content here...",
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z",
  "actif": true
}

// Global Post Response (with media)
{
  "uuid": "01234567-89ab-cdef-0123-456789abcdef",
  "title": "My Blog Post",
  "content": "Post content here...",
  "created_at": "2025-01-01T12:00:00Z",
  "updated_at": "2025-01-01T12:00:00Z",
  "actif": true,
  "postImagePost": [
    {
      "uuid": "image-uuid-here",
      "label": "My Image",
      "image": "/media/images/filename.jpg"
    }
  ],
  "postVideoPost": [],
  "postAudioPost": [],
  "postFilePost": []
}
```

## 🤝 Development Workflow

### Adding New Features
1. **Update Models**: Modify `models.py` and create migrations
2. **Create Serializers**: Add to `api/serializers.py`
3. **Implement Views**: Add to `api/views.py`
4. **Update URLs**: Register endpoints in `api/urls.py`
5. **Test API**: Use Django admin and curl commands

### Code Quality
```bash
# Format code
pip install black
black .

# Lint code
pip install flake8
flake8 .

# Type checking
pip install mypy django-stubs
mypy .
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [JWT Authentication](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Django CORS Headers](https://github.com/adamchainz/django-cors-headers)

---

**Django Backend v1.0 - Built with Django 5.2 + DRF**