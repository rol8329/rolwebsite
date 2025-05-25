# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.http import Http404
from django.db.models import Q

from spectacle.models import Presentation, Slide, SlideElement, PresentationTemplate
from .serializers import (
    PresentationListSerializer, PresentationDetailSerializer,
    PresentationCreateUpdateSerializer, SlideSerializer,
    SlideCreateUpdateSerializer, SlideElementSerializer,
    PresentationTemplateSerializer, PresentationCloneSerializer,
    BulkSlideUpdateSerializer, PresentationExportSerializer
)


class PresentationListCreateAPIView(APIView):
    """List all presentations or create a new presentation"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        # Filter presentations based on user permissions
        if request.user.is_authenticated:
            presentations = Presentation.objects.filter(
                Q(author=request.user) | Q(is_public=True)
            )
        else:
            presentations = Presentation.objects.filter(is_public=True)

        # Optional filtering
        search = request.query_params.get('search', None)
        if search:
            presentations = presentations.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )

        author_id = request.query_params.get('author', None)
        if author_id:
            presentations = presentations.filter(author_id=author_id)

        tag = request.query_params.get('tag', None)
        if tag:
            presentations = presentations.filter(tags__contains=[tag])

        serializer = PresentationListSerializer(presentations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PresentationCreateUpdateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            presentation = serializer.save()
            detail_serializer = PresentationDetailSerializer(presentation)
            return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PresentationDetailAPIView(APIView):
    """Retrieve, update or delete a presentation"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self, pk, user):
        try:
            presentation = Presentation.objects.get(pk=pk)
            # Check permissions
            if presentation.author != user and not presentation.is_public:
                raise Http404
            return presentation
        except Presentation.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        presentation = self.get_object(pk, request.user)
        serializer = PresentationDetailSerializer(presentation)
        return Response(serializer.data)

    def put(self, request, pk):
        presentation = self.get_object(pk, request.user)
        # Only author can update
        if presentation.author != request.user:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PresentationCreateUpdateSerializer(
            presentation,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            presentation = serializer.save()
            detail_serializer = PresentationDetailSerializer(presentation)
            return Response(detail_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        presentation = self.get_object(pk, request.user)
        # Only author can delete
        if presentation.author != request.user:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        presentation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PresentationCloneAPIView(APIView):
    """Clone an existing presentation"""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            original = Presentation.objects.get(pk=pk)
            # Check if user can access the presentation
            if original.author != request.user and not original.is_public:
                return Response(
                    {"error": "Permission denied"},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Presentation.DoesNotExist:
            raise Http404

        serializer = PresentationCloneSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                # Create new presentation
                clone_data = serializer.validated_data
                new_presentation = Presentation.objects.create(
                    title=clone_data['title'],
                    description=clone_data.get('description', original.description),
                    author=request.user,
                    is_public=clone_data.get('is_public', False),
                    theme=original.theme,
                    template=original.template,
                    transition=original.transition,
                    background_color=original.background_color,
                    text_color=original.text_color,
                    tags=original.tags.copy()
                )

                # Clone slides if requested
                if clone_data.get('clone_slides', True):
                    for slide in original.slides.all():
                        new_slide = Slide.objects.create(
                            presentation=new_presentation,
                            slide_type=slide.slide_type,
                            order=slide.order,
                            title=slide.title,
                            content=slide.content,
                            subtitle=slide.subtitle,
                            background_color=slide.background_color,
                            text_color=slide.text_color,
                            font_size=slide.font_size,
                            text_align=slide.text_align,
                            transition=slide.transition,
                            animation=slide.animation,
                            custom_css=slide.custom_css,
                            layout_config=slide.layout_config.copy(),
                            notes=slide.notes
                        )

                        # Clone elements if requested
                        if clone_data.get('clone_elements', True):
                            for element in slide.elements.all():
                                SlideElement.objects.create(
                                    slide=new_slide,
                                    element_type=element.element_type,
                                    order=element.order,
                                    content=element.content,
                                    alt_text=element.alt_text,
                                    x_position=element.x_position,
                                    y_position=element.y_position,
                                    width=element.width,
                                    height=element.height,
                                    font_family=element.font_family,
                                    font_size=element.font_size,
                                    font_weight=element.font_weight,
                                    color=element.color,
                                    background_color=element.background_color,
                                    border_style=element.border_style,
                                    animation=element.animation,
                                    animation_delay=element.animation_delay,
                                    properties=element.properties.copy()
                                )

            detail_serializer = PresentationDetailSerializer(new_presentation)
            return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PresentationExportAPIView(APIView):
    """Export presentation in Spectacle format"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            presentation = Presentation.objects.get(pk=pk)
            # Check permissions
            if presentation.author != request.user and not presentation.is_public:
                return Response(
                    {"error": "Permission denied"},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Presentation.DoesNotExist:
            raise Http404

        serializer = PresentationExportSerializer(presentation)
        return Response(serializer.data)


class SlideListCreateAPIView(APIView):
    """List slides for a presentation or create a new slide"""
    permission_classes = [IsAuthenticated]

    def get_presentation(self, pk, user):
        try:
            presentation = Presentation.objects.get(pk=pk)
            if presentation.author != user and not presentation.is_public:
                raise Http404
            return presentation
        except Presentation.DoesNotExist:
            raise Http404

    def get(self, request, presentation_pk):
        presentation = self.get_presentation(presentation_pk, request.user)
        slides = presentation.slides.all()
        serializer = SlideSerializer(slides, many=True)
        return Response(serializer.data)

    def post(self, request, presentation_pk):
        presentation = self.get_presentation(presentation_pk, request.user)
        # Only author can add slides
        if presentation.author != request.user:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SlideCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            slide = serializer.save(presentation=presentation)
            detail_serializer = SlideSerializer(slide)
            return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlideDetailAPIView(APIView):
    """Retrieve, update or delete a slide"""
    permission_classes = [IsAuthenticated]

    def get_object(self, presentation_pk, slide_pk, user):
        try:
            slide = Slide.objects.select_related('presentation').get(
                presentation_id=presentation_pk,
                pk=slide_pk
            )
            if slide.presentation.author != user and not slide.presentation.is_public:
                raise Http404
            return slide
        except Slide.DoesNotExist:
            raise Http404

    def get(self, request, presentation_pk, slide_pk):
        slide = self.get_object(presentation_pk, slide_pk, request.user)
        serializer = SlideSerializer(slide)
        return Response(serializer.data)

    def put(self, request, presentation_pk, slide_pk):
        slide = self.get_object(presentation_pk, slide_pk, request.user)
        # Only author can update
        if slide.presentation.author != request.user:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SlideCreateUpdateSerializer(slide, data=request.data)
        if serializer.is_valid():
            slide = serializer.save()
            detail_serializer = SlideSerializer(slide)
            return Response(detail_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, presentation_pk, slide_pk):
        slide = self.get_object(presentation_pk, slide_pk, request.user)
        # Only author can delete
        if slide.presentation.author != request.user:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        slide.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SlideBulkUpdateAPIView(APIView):
    """Bulk update slide orders"""
    permission_classes = [IsAuthenticated]

    def put(self, request, presentation_pk):
        try:
            presentation = Presentation.objects.get(pk=presentation_pk)
            if presentation.author != request.user:
                return Response(
                    {"error": "Permission denied"},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Presentation.DoesNotExist:
            raise Http404

        serializer = BulkSlideUpdateSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                slides_data = serializer.validated_data['slides']
                for slide_data in slides_data:
                    try:
                        slide = Slide.objects.get(
                            id=slide_data['id'],
                            presentation=presentation
                        )
                        slide.order = slide_data['order']
                        slide.save(update_fields=['order'])
                    except Slide.DoesNotExist:
                        return Response(
                            {"error": f"Slide {slide_data['id']} not found"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

            # Return updated slides
            slides = presentation.slides.all()
            serializer = SlideSerializer(slides, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlideElementListCreateAPIView(APIView):
    """List elements for a slide or create a new element"""
    permission_classes = [IsAuthenticated]

    def get_slide(self, presentation_pk, slide_pk, user):
        try:
            slide = Slide.objects.select_related('presentation').get(
                presentation_id=presentation_pk,
                pk=slide_pk
            )
            if slide.presentation.author != user and not slide.presentation.is_public:
                raise Http404
            return slide
        except Slide.DoesNotExist:
            raise Http404

    def get(self, request, presentation_pk, slide_pk):
        slide = self.get_slide(presentation_pk, slide_pk, request.user)
        elements = slide.elements.all()
        serializer = SlideElementSerializer(elements, many=True)
        return Response(serializer.data)

    def post(self, request, presentation_pk, slide_pk):
        slide = self.get_slide(presentation_pk, slide_pk, request.user)
        # Only author can add elements
        if slide.presentation.author != request.user:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SlideElementSerializer(data=request.data)
        if serializer.is_valid():
            element = serializer.save(slide=slide)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SlideElementDetailAPIView(APIView):
    """Retrieve, update or delete a slide element"""
    permission_classes = [IsAuthenticated]

    def get_object(self, presentation_pk, slide_pk, element_pk, user):
        try:
            element = SlideElement.objects.select_related('slide__presentation').get(
                slide__presentation_id=presentation_pk,
                slide_id=slide_pk,
                pk=element_pk
            )
            if (element.slide.presentation.author != user and
                    not element.slide.presentation.is_public):
                raise Http404
            return element
        except SlideElement.DoesNotExist:
            raise Http404

    def get(self, request, presentation_pk, slide_pk, element_pk):
        element = self.get_object(presentation_pk, slide_pk, element_pk, request.user)
        serializer = SlideElementSerializer(element)
        return Response(serializer.data)

    def put(self, request, presentation_pk, slide_pk, element_pk):
        element = self.get_object(presentation_pk, slide_pk, element_pk, request.user)
        # Only author can update
        if element.slide.presentation.author != request.user:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SlideElementSerializer(element, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, presentation_pk, slide_pk, element_pk):
        element = self.get_object(presentation_pk, slide_pk, element_pk, request.user)
        # Only author can delete
        if element.slide.presentation.author != request.user:
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        element.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PresentationTemplateListCreateAPIView(APIView):
    """List all templates or create a new template"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        templates = PresentationTemplate.objects.filter(
            Q(author=request.user) | Q(is_public=True)
        )
        serializer = PresentationTemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PresentationTemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)