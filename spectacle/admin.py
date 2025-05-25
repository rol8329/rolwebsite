# admin.py
from django.contrib import admin
from .models import Presentation, Slide, SlideElement, PresentationTemplate


class SlideElementInline(admin.TabularInline):
    model = SlideElement
    extra = 0
    fields = ['element_type', 'order', 'content', 'x_position', 'y_position', 'width', 'height']
    ordering = ['order']


class SlideInline(admin.StackedInline):
    model = Slide
    extra = 0
    fields = ['slide_type', 'order', 'title', 'content', 'background_color', 'notes']
    ordering = ['order']


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slide_count', 'is_public', 'created_at', 'updated_at']
    list_filter = ['is_public', 'theme', 'created_at', 'author']
    search_fields = ['title', 'description', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'slide_count']
    inlines = [SlideInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'author', 'is_public', 'tags')
        }),
        ('Spectacle Settings', {
            'fields': ('theme', 'template', 'transition', 'background_color', 'text_color')
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'slide_count'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slide_type', 'presentation', 'order', 'created_at']
    list_filter = ['slide_type', 'presentation__title', 'created_at']
    search_fields = ['title', 'content', 'presentation__title']
    ordering = ['presentation', 'order']
    inlines = [SlideElementInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('presentation', 'slide_type', 'order', 'title', 'content', 'subtitle')
        }),
        ('Styling', {
            'fields': ('background_color', 'background_image', 'text_color', 'font_size', 'text_align')
        }),
        ('Animation', {
            'fields': ('transition', 'animation')
        }),
        ('Advanced', {
            'fields': ('custom_css', 'layout_config', 'notes'),
            'classes': ('collapse',)
        })
    )


@admin.register(SlideElement)
class SlideElementAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'element_type', 'slide', 'order']
    list_filter = ['element_type', 'slide__presentation__title']
    search_fields = ['content', 'slide__title', 'slide__presentation__title']
    ordering = ['slide', 'order']

    fieldsets = (
        ('Basic Information', {
            'fields': ('slide', 'element_type', 'order', 'content', 'alt_text')
        }),
        ('Position & Size', {
            'fields': ('x_position', 'y_position', 'width', 'height')
        }),
        ('Styling', {
            'fields': ('font_family', 'font_size', 'font_weight', 'color', 'background_color', 'border_style')
        }),
        ('Animation', {
            'fields': ('animation', 'animation_delay')
        }),
        ('Advanced', {
            'fields': ('properties',),
            'classes': ('collapse',)
        })
    )


@admin.register(PresentationTemplate)
class PresentationTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'is_public', 'created_at']
    list_filter = ['is_public', 'theme', 'created_at']
    search_fields = ['name', 'description', 'author__username']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'author', 'is_public')
        }),
        ('Styling', {
            'fields': ('theme', 'background_color', 'text_color', 'font_family')
        }),
        ('Template Structure', {
            'fields': ('structure', 'custom_css'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.author = request.user
        super().save_model(request, obj, form, change)


# ==============================================================================
# SETUP INSTRUCTIONS
# ==============================================================================

"""
INSTALLATION AND SETUP INSTRUCTIONS:

1. Add the app to your INSTALLED_APPS in settings.py:
   INSTALLED_APPS = [
       ...
       'presentations',  # Your app name
       'rest_framework',
   ]

2. Configure DRF in settings.py:
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.SessionAuthentication',
           'rest_framework.authentication.TokenAuthentication',
       ],
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
       'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
       'PAGE_SIZE': 20
   }

3. Configure media files in settings.py:
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

4. Add to your main urls.py:
   from django.conf import settings
   from django.conf.urls.static import static

   urlpatterns = [
       ...
       path('api/', include('presentations.urls')),
   ]

   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

5. Create and run migrations:
   python manage.py makemigrations presentations
   python manage.py migrate

6. Create a superuser (optional):
   python manage.py createsuperuser

7. Install required packages:
   pip install djangorestframework
   pip install Pillow  # For image fields

8. Optional - Install CORS headers for React frontend:
   pip install django-cors-headers

   Add to INSTALLED_APPS:
   'corsheaders',

   Add to MIDDLEWARE (at the top):
   'corsheaders.middleware.CorsMiddleware',

   Add CORS settings:
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",  # React dev server
       "http://127.0.0.1:3000",
   ]

API USAGE EXAMPLES:

# Create a presentation
POST /api/presentations/
{
    "title": "My First Presentation",
    "description": "A sample presentation",
    "theme": "default",
    "is_public": false
}

# Add a slide
POST /api/presentations/1/slides/
{
    "slide_type": "title",
    "order": 1,
    "title": "Welcome",
    "content": "Welcome to my presentation",
    "background_color": "#ffffff"
}

# Add an element to a slide
POST /api/presentations/1/slides/1/elements/
{
    "element_type": "text",
    "order": 1,
    "content": "Hello World!",
    "x_position": 50,
    "y_position": 50,
    "width": 200,
    "height": 100
}

# Clone a presentation
POST /api/presentations/1/clone/
{
    "title": "Cloned Presentation",
    "clone_slides": true,
    "clone_elements": true
}

# Export for Spectacle
GET /api/presentations/1/export/
"""
