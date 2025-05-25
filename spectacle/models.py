# models.py
from django.db import models
from django.contrib.auth.models import User
import json


class Presentation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presentations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    # Spectacle-specific settings
    theme = models.CharField(max_length=50, default='default')
    template = models.CharField(max_length=50, default='default')
    transition = models.CharField(max_length=50, default='slide')
    background_color = models.CharField(max_length=7, default='#ffffff')
    text_color = models.CharField(max_length=7, default='#000000')

    # Metadata
    tags = models.JSONField(default=list, blank=True)
    thumbnail = models.ImageField(upload_to='presentation_thumbnails/', blank=True, null=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    @property
    def slide_count(self):
        return self.slides.count()


class Slide(models.Model):
    SLIDE_TYPES = [
        ('title', 'Title Slide'),
        ('content', 'Content Slide'),
        ('image', 'Image Slide'),
        ('code', 'Code Slide'),
        ('quote', 'Quote Slide'),
        ('two_column', 'Two Column Slide'),
        ('list', 'List Slide'),
        ('custom', 'Custom Slide'),
    ]

    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name='slides')
    slide_type = models.CharField(max_length=20, choices=SLIDE_TYPES, default='content')
    order = models.PositiveIntegerField()

    # Content fields
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    subtitle = models.CharField(max_length=200, blank=True)

    # Spectacle-specific properties
    background_color = models.CharField(max_length=7, blank=True)
    background_image = models.ImageField(upload_to='slide_backgrounds/', blank=True, null=True)
    text_color = models.CharField(max_length=7, blank=True)
    font_size = models.CharField(max_length=20, blank=True)
    text_align = models.CharField(max_length=20, default='left')

    # Transition and animation
    transition = models.CharField(max_length=50, blank=True)
    animation = models.CharField(max_length=50, blank=True)

    # Custom styling and layout
    custom_css = models.TextField(blank=True)
    layout_config = models.JSONField(default=dict, blank=True)

    # Speaker notes
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ['presentation', 'order']

    def __str__(self):
        return f"{self.presentation.title} - Slide {self.order}"


class SlideElement(models.Model):
    """Individual elements within a slide (text blocks, images, code blocks, etc.)"""
    ELEMENT_TYPES = [
        ('text', 'Text Block'),
        ('heading', 'Heading'),
        ('image', 'Image'),
        ('code', 'Code Block'),
        ('list', 'List'),
        ('link', 'Link'),
        ('video', 'Video'),
        ('chart', 'Chart'),
        ('shape', 'Shape'),
    ]

    slide = models.ForeignKey(Slide, on_delete=models.CASCADE, related_name='elements')
    element_type = models.CharField(max_length=20, choices=ELEMENT_TYPES)
    order = models.PositiveIntegerField()

    # Content
    content = models.TextField()
    alt_text = models.CharField(max_length=200, blank=True)  # For accessibility

    # Positioning and sizing
    x_position = models.FloatField(default=0)
    y_position = models.FloatField(default=0)
    width = models.FloatField(default=100)
    height = models.FloatField(default=50)

    # Styling
    font_family = models.CharField(max_length=100, blank=True)
    font_size = models.CharField(max_length=20, blank=True)
    font_weight = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=7, blank=True)
    background_color = models.CharField(max_length=7, blank=True)
    border_style = models.CharField(max_length=100, blank=True)

    # Animation and effects
    animation = models.CharField(max_length=50, blank=True)
    animation_delay = models.FloatField(default=0)

    # Additional properties (for flexibility)
    properties = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['order']
        unique_together = ['slide', 'order']

    def __str__(self):
        return f"{self.slide} - {self.element_type} {self.order}"


class PresentationTemplate(models.Model):
    """Reusable presentation templates"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='templates')

    # Template configuration
    theme = models.CharField(max_length=50, default='default')
    background_color = models.CharField(max_length=7, default='#ffffff')
    text_color = models.CharField(max_length=7, default='#000000')
    font_family = models.CharField(max_length=100, default='Arial, sans-serif')

    # Template structure (JSON defining slide layouts)
    structure = models.JSONField(default=dict)

    # Style overrides
    custom_css = models.TextField(blank=True)

    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
# Create your models here.
