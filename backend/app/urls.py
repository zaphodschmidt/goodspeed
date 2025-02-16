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
    path('upload/', views.upload_image, name='upload_image_api'),
    path('occupiedParkMoblie/', views.getOccupiedSpots, name='check_occupied_spots'),
    path('parkingSpotsOpen/<int:building_id>/<str:location>', views.getParkingSpotsOpen, name='get_parking_spots_open'),
    path('api/camera/<int:building_id>/<str:location>/<int:cam_num>', views.addLocationToCamera , name='add_location_to_camera')
]