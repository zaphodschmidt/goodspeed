# toolsapp/urls.py
# Sets up URL routing for the app. Defines how different URL patterns should be used by different views.

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Viewsets
router = DefaultRouter()
router.register(r'buildings', views.BuildingViewSet, basename='buildings') 
router.register(r'cameras', views.CameraViewSet, basename='cameras') 
router.register(r'parking_spots', views.ParkingSpotViewSet, basename='parking_spots') 
router.register(r'vertices', views.VertexViewSet, basename='vertices') 

urlpatterns = [
    path('', include(router.urls)), 
]