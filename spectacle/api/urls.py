# urls.py
from django.urls import path
from .views import (
    PresentationListCreateAPIView, PresentationDetailAPIView,
    PresentationCloneAPIView, PresentationExportAPIView,
    SlideListCreateAPIView, SlideDetailAPIView, SlideBulkUpdateAPIView,
    SlideElementListCreateAPIView, SlideElementDetailAPIView,
    PresentationTemplateListCreateAPIView
)

app_name = 'presentations'

urlpatterns = [
    # Presentation endpoints
    path('presentations/',
         PresentationListCreateAPIView.as_view(),
         name='presentation-list-create'),

    path('presentations/<int:pk>/',
         PresentationDetailAPIView.as_view(),
         name='presentation-detail'),

    path('presentations/<int:pk>/clone/',
         PresentationCloneAPIView.as_view(),
         name='presentation-clone'),

    path('presentations/<int:pk>/export/',
         PresentationExportAPIView.as_view(),
         name='presentation-export'),

    # Slide endpoints
    path('presentations/<int:presentation_pk>/slides/',
         SlideListCreateAPIView.as_view(),
         name='slide-list-create'),

    path('presentations/<int:presentation_pk>/slides/<int:slide_pk>/',
         SlideDetailAPIView.as_view(),
         name='slide-detail'),

    path('presentations/<int:presentation_pk>/slides/bulk-update/',
         SlideBulkUpdateAPIView.as_view(),
         name='slide-bulk-update'),

    # Slide element endpoints
    path('presentations/<int:presentation_pk>/slides/<int:slide_pk>/elements/',
         SlideElementListCreateAPIView.as_view(),
         name='slide-element-list-create'),

    path('presentations/<int:presentation_pk>/slides/<int:slide_pk>/elements/<int:element_pk>/',
         SlideElementDetailAPIView.as_view(),
         name='slide-element-detail'),

    # Template endpoints
    path('templates/',
         PresentationTemplateListCreateAPIView.as_view(),
         name='template-list-create'),
]

# Example usage patterns:
# GET /api/presentations/ - List all presentations
# POST /api/presentations/ - Create new presentation
# GET /api/presentations/1/ - Get specific presentation with all slides
# PUT /api/presentations/1/ - Update presentation
# DELETE /api/presentations/1/ - Delete presentation
# POST /api/presentations/1/clone/ - Clone presentation
# GET /api/presentations/1/export/ - Export in Spectacle format

# GET /api/presentations/1/slides/ - List slides for presentation
# POST /api/presentations/1/slides/ - Create new slide
# GET /api/presentations/1/slides/1/ - Get specific slide
# PUT /api/presentations/1/slides/1/ - Update slide
# DELETE /api/presentations/1/slides/1/ - Delete slide
# PUT /api/presentations/1/slides/bulk-update/ - Update slide orders

# GET /api/presentations/1/slides/1/elements/ - List elements for slide
# POST /api/presentations/1/slides/1/elements/ - Create new element
# GET /api/presentations/1/slides/1/elements/1/ - Get specific element
# PUT /api/presentations/1/slides/1/elements/1/ - Update element
# DELETE /api/presentations/1/slides/1/elements/1/ - Delete element

# GET /api/templates/ - List all templates
# POST /api/templates/ - Create new template