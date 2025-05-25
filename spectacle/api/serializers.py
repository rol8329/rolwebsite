# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from spectacle.models import Presentation, Slide, SlideElement, PresentationTemplate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class SlideElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlideElement
        fields = [
            'id', 'element_type', 'order', 'content', 'alt_text',
            'x_position', 'y_position', 'width', 'height',
            'font_family', 'font_size', 'font_weight', 'color',
            'background_color', 'border_style', 'animation',
            'animation_delay', 'properties'
        ]


class SlideSerializer(serializers.ModelSerializer):
    elements = SlideElementSerializer(many=True, read_only=True)

    class Meta:
        model = Slide
        fields = [
            'id', 'slide_type', 'order', 'title', 'content', 'subtitle',
            'background_color', 'background_image', 'text_color',
            'font_size', 'text_align', 'transition', 'animation',
            'custom_css', 'layout_config', 'notes', 'elements',
            'created_at', 'updated_at'
        ]


class SlideCreateUpdateSerializer(serializers.ModelSerializer):
    """Separate serializer for creating/updating slides without nested elements"""

    class Meta:
        model = Slide
        fields = [
            'slide_type', 'order', 'title', 'content', 'subtitle',
            'background_color', 'background_image', 'text_color',
            'font_size', 'text_align', 'transition', 'animation',
            'custom_css', 'layout_config', 'notes'
        ]


class PresentationListSerializer(serializers.ModelSerializer):
    """Lighter serializer for listing presentations"""
    author = UserSerializer(read_only=True)
    slide_count = serializers.ReadOnlyField()

    class Meta:
        model = Presentation
        fields = [
            'id', 'title', 'description', 'author', 'created_at',
            'updated_at', 'is_public', 'theme', 'tags', 'thumbnail',
            'slide_count'
        ]


class PresentationDetailSerializer(serializers.ModelSerializer):
    """Full serializer with all slides and elements"""
    author = UserSerializer(read_only=True)
    slides = SlideSerializer(many=True, read_only=True)
    slide_count = serializers.ReadOnlyField()

    class Meta:
        model = Presentation
        fields = [
            'id', 'title', 'description', 'author', 'created_at',
            'updated_at', 'is_public', 'theme', 'template', 'transition',
            'background_color', 'text_color', 'tags', 'thumbnail',
            'slide_count', 'slides'
        ]


class PresentationCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating presentations"""

    class Meta:
        model = Presentation
        fields = [
            'title', 'description', 'is_public', 'theme', 'template',
            'transition', 'background_color', 'text_color', 'tags',
            'thumbnail'
        ]

    def create(self, validated_data):
        # Set the author to the current user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PresentationTemplateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = PresentationTemplate
        fields = [
            'id', 'name', 'description', 'author', 'theme',
            'background_color', 'text_color', 'font_family',
            'structure', 'custom_css', 'is_public', 'created_at'
        ]


class PresentationCloneSerializer(serializers.Serializer):
    """Serializer for cloning presentations"""
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, allow_blank=True)
    is_public = serializers.BooleanField(default=False)
    clone_slides = serializers.BooleanField(default=True)
    clone_elements = serializers.BooleanField(default=True)


class BulkSlideUpdateSerializer(serializers.Serializer):
    """Serializer for bulk updating slide orders"""
    slides = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )

    def validate_slides(self, value):
        """Ensure slide data is valid"""
        for slide_data in value:
            if 'id' not in slide_data or 'order' not in slide_data:
                raise serializers.ValidationError(
                    "Each slide must have 'id' and 'order' fields"
                )
        return value


class PresentationExportSerializer(serializers.ModelSerializer):
    """Serializer for exporting presentations in Spectacle format"""
    author = UserSerializer(read_only=True)
    slides = SlideSerializer(many=True, read_only=True)

    class Meta:
        model = Presentation
        fields = [
            'id', 'title', 'description', 'author', 'theme', 'template',
            'transition', 'background_color', 'text_color', 'tags',
            'slides', 'created_at', 'updated_at'
        ]

    def to_representation(self, instance):
        """Convert to Spectacle-compatible format"""
        data = super().to_representation(instance)

        # Transform to Spectacle format
        spectacle_data = {
            'metadata': {
                'title': data['title'],
                'description': data['description'],
                'author': data['author']['username'] if data['author'] else '',
                'theme': data['theme'],
                'template': data['template'],
                'transition': data['transition'],
                'backgroundColor': data['background_color'],
                'textColor': data['text_color'],
                'tags': data['tags'],
                'createdAt': data['created_at'],
                'updatedAt': data['updated_at']
            },
            'slides': []
        }

        # Transform slides
        for slide in data['slides']:
            spectacle_slide = {
                'id': slide['id'],
                'type': slide['slide_type'],
                'title': slide['title'],
                'content': slide['content'],
                'subtitle': slide['subtitle'],
                'backgroundColor': slide['background_color'],
                'backgroundImage': slide['background_image'],
                'textColor': slide['text_color'],
                'fontSize': slide['font_size'],
                'textAlign': slide['text_align'],
                'transition': slide['transition'],
                'animation': slide['animation'],
                'customCSS': slide['custom_css'],
                'layoutConfig': slide['layout_config'],
                'notes': slide['notes'],
                'elements': slide['elements']
            }
            spectacle_data['slides'].append(spectacle_slide)

        return spectacle_data