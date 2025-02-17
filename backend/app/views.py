from rest_framework import viewsets
from rest_framework.decorators import action
from .models import *
from .serializers import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from app.models import Building, Camera, ParkingSpot, Vertex
from .services.parking_detection import ParkingDetection
from .services.parking_paymentCheking import PaymentChecking
from .tasks import run_parking_detection
import os
import json
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

PARKMOBILE_AVALON_USERNAME = os.environ.get("PARKMOBILE_AVALON_USERNAME")
PARKMOBILE_AVALON_PASSWORD = os.environ.get("PARKMOBILE_AVALON_PASSWORD")
PARKMOBILE_CAPI_USERNAME = os.environ.get("PARKMOBILE_CAPI_USERNAME")
PARKMOBILE_CAPI_PASSWORD = os.environ.get("PARKMOBILE_CAPI_PASSWORD")
PARKMOBILE_NY_USERNAME = os.environ.get("PARKMOBILE_NY_USERNAME")
PARKMOBILE_NY_PASSWORD = os.environ.get("PARKMOBILE_NY_PASSWORD")
PARKMOBILE_APIKEY = os.environ.get("PARKMOBILE_APIKEY")

class BuildingViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

class CameraViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class ParkingSpotViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = ParkingSpot.objects.all()
    serializer_class = ParkingSpotSerializer

class VertexViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = Vertex.objects.all()
    serializer_class = VertexSerializer

class LocationViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.AllowAny]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    @action(detail=False, methods=['get'], name="occupancyForLocation")
    def occupancyForLocation(self, request):
        location_name = request.query_params.get('location_name')
        building_name = request.query_params.get('building_name')

        if location_name and building_name:
            return JsonResponse({'error':'location_name and building_name are required'}, status=400)
        
        building_obj = get_object_or_404(Building, building_name = building_name)
        location_obj = get_object_or_404(Location, location_name = location_name)

        try:
            cameras = Camera.objects.filter(building = building_obj, location = location_obj)
        except Exception as e:
            print(f"Error: Cameras could not be found \n {e}!")
            raise

        try:
            parkingSpots = ParkingSpot.objects.filter(camera__in = cameras)
            parkingSpots = ParkingSpotSerializer(parkingSpots, many=True).data
        except Exception as e:
            print(f"Error: Parking Spots could not be found \n {e}!")
            raise

        occupiedSpots = 0
        totalSpots = 0
        for spot in parkingSpots:
            if spot['occupied']:
                occupiedSpots+=1
            totalSpots+=1

        return JsonResponse({
            'location':location_name,
            'totalSpots': totalSpots,
            'occupiedSpots': occupiedSpots
        })
    
    @action(detail=False, methods=['get'], name='buildinglocations')
    def buildinglocations(self,request):
        print(f"NAME: {request.query_params.get('building_name')}")
        building_name = request.query_params.get('building_name')
        if not building_name:
            return JsonResponse(
                {'error':'building_name is required'},
                status=400
            )

        try:
            building_obj = Building.objects.get(name=building_name)
        except Building.DoesNotExist:
            return JsonResponse(
                {'error':f'Building name {building_name} not found!'},
                status=400
            )
        
        locations = Location.objects.filter(building=building_obj)
        locations_data = LocationSerializer(locations, many=True).data
        
        return JsonResponse({
            'locations': locations_data
        })

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)

        image = request.FILES.get('image')  # Safely get the image
        cam_num = request.POST.get('cam_num')
        building_name = request.POST.get('building_name')

        if not image or not cam_num or not building_name:
            return JsonResponse({'error': 'image, cam_num, and building_name are required'}, status=400)
        
        try:
            # Find the Camera
            camera = Camera.objects.get(cam_num=cam_num, building__name=building_name)
        except Camera.DoesNotExist:
            return JsonResponse({'error': 'Camera not found'}, status=404)

        # Handle image replacement
        new_image = Image.objects.create(image=image)

        if camera.image:
            # Delete the old image file
            if camera.image.image and default_storage.exists(camera.image.image.path):
                default_storage.delete(camera.image.image.path)
            # Delete the old image model instance
            camera.image.delete()

        camera.image = new_image
        camera.save()

        # Run parking detection on the uploaded image
        image_path = new_image.image.path  # Get the path to the saved image
        image_path = os.path.abspath(new_image.image.path)
        print(f"Absolute image path: {image_path}")
        run_parking_detection.delay(image_path, cam_num, building_name)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'camera_id': camera.id,
            'new_image_url': new_image.image.url,
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def getOccupiedSpots(request):
    if request.method == "GET":
        pay = PaymentChecking(PARKMOBILE_AVALON_USERNAME, PARKMOBILE_AVALON_PASSWORD, PARKMOBILE_APIKEY)
        spots = pay.checkOccupiedspot_zone("Vertex","9163")
        print(spots)
        return JsonResponse({
            'message': 'Spots Found Successfully',
            'spots': spots,
        })