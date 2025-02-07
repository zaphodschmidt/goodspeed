from rest_framework import viewsets
from .models import *
from .serializers import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from app.models import Building, Camera, ParkingSpot, Vertex
from .services.parking_management import ParkingManagement
import os

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
        parking_management = ParkingManagement(model_path='yolov8n.pt')
        parking_management.runParkingDetection(image_path)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'camera_id': camera.id,
            'new_image_url': new_image.image.url,
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)



