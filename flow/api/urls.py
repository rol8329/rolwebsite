# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlowChartViewSet

router = DefaultRouter()
router.register(r'flowcharts', FlowChartViewSet, basename='flowchart')

urlpatterns = [
    path('api/', include(router.urls)),
]