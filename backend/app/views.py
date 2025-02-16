from rest_framework import viewsets
from .models import *
from .serializers import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
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

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
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
        
        if camera.image:
            # Delete the old image from S3
            if camera.image.image:
                camera.image.image.delete(save=False)
            camera.image.delete()


        # Handle image replacement
        new_image = Image.objects.create(image=image)

        
        camera.image = new_image
        camera.save()

        # Run parking detection on the uploaded image
        run_parking_detection.delay(camera.id)

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