# from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from django.http import JsonResponse
from rest_framework import status, permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.storage import default_storage
import os
from PIL import Image as PILImage
import cv2
import numpy as np
import json
from ultralytics import solutions
from ultralytics.solutions.solutions import BaseSolution
from ultralytics.utils import LOGGER
from ultralytics.utils.checks import check_requirements
from ultralytics.utils.plotting import Annotator
from app.models import Building, Camera, ParkingSpot, Vertex
from django.db import transaction

#consts
MODEL = 'yolov8n.pt'

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

class ParkingManagement(BaseSolution):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.json = None
        self.pr_info = {"Occupancy": 0, "Available": 0}

        self.arc = (0, 0, 255)
        self.occ = (0, 255, 0)
        self.dc = (255, 0, 189)

        self.normalImgW = 2560
        self.normalImgH = 1920
        self.webpageImgW = 1000
        self.webpageImgH = 750

    def loadCameraVertices(self, photo: str):
        # Extract building name and camera number from the filename
        buildingName = photo.split('_')[3]
        cameraNumStr = photo.split('_')[4]  # This will be "cam11.jpeg"
        cameraNum = int(cameraNumStr[3:].split('.')[0])  # Remove "cam" and ".jpeg"
        
        print("bruh", cameraNum)

        if buildingName.lower() == "vertex1":
            buildingName = "Vertex"

        try:
            building = Building.objects.get(name=buildingName)
        except Building.DoesNotExist:
            print(f"Building '{buildingName}' does not exist.")
            return

        try:
            camera = building.cameras.get(cam_num=cameraNum)
        except Camera.DoesNotExist:
            print(f"Camera {cameraNum} does not exist in building {building.name}.")
            return

        #calc how much the boudning boxes need to be scaled
        scaleW = self.normalImgW / self.webpageImgW
        scaleH = self.normalImgH / self.webpageImgH

        parkingSpotBounds = []
        self.spot_ids = []

        for spot in camera.parking_spots.all():
            print(f"Found parking spot: {spot}")
            if not spot.vertices.exists():
                print(f"Parking spot {spot.id} has no vertices.")
            else:
                pointsDict = {"points": []}
                for point in spot.vertices.all():
                    pointsDict["points"].append([point.x * scaleW, point.y * scaleH])
                parkingSpotBounds.append(pointsDict)
                self.spot_ids.append(spot.id)

        # jsonData = json.dumps(parkingSpotBounds)
        # with open('vertexes.json', 'w') as f:
        #     f.write(jsonData)

        print(f"Loaded parking spots: {self.spot_ids}")
        return parkingSpotBounds




    def isJpeg(self, file_path:str):
        try:
            with PILImage.open(file_path) as img:
                return img.format == 'JPEG'
        except (IOError, OSError):
            return False

    def getDirs(self, path: str):
        files = []
        for fileName in os.scandir(path):
            if fileName.is_file() and self.isJpeg(fileName):
                files.append(path+"/"+fileName.name)
        return files

    def process_data(self, im0):
        if not self.json:
            print("No parking spot data loaded.")
            return im0
    
        self.extract_tracks(im0)  # extract tracks from im0
        es, fs = len(self.json), 0  # empty slots, filled slots
        annotator = Annotator(im0, self.line_width)  # init annotator

        parking_spots_to_update = []

        for region , spot_id in zip(self.json, self.spot_ids):
            # Convert points to a NumPy array with the correct dtype and reshape properly
            pts_array = np.array(region["points"], dtype=np.int32).reshape((-1, 1, 2))
            rg_occupied = False  # occupied region initialization
            for box, cls in zip(self.boxes, self.clss):
                xc, yc = int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)
                dist = cv2.pointPolygonTest(pts_array, (xc, yc), False)
                if dist >= 0:
                    # cv2.circle(im0, (xc, yc), radius=self.line_width * 4, color=self.dc, thickness=-1)
                    annotator.display_objects_labels(
                        im0, self.model.names[int(cls)], (104, 31, 17), (255, 255, 255), xc, yc, 10
                    )
                    rg_occupied = True
                    break
            fs, es = (fs + 1, es - 1) if rg_occupied else (fs, es)
            # Plotting regions
            cv2.polylines(im0, [pts_array], isClosed=True, color=self.occ if rg_occupied else self.arc, thickness=2)

            parking_spots_to_update.append({"spot_id": spot_id, "occupied": rg_occupied})
            
        with transaction.atomic():
            for spot in parking_spots_to_update:
                ParkingSpot.objects.filter(id=spot["spot_id"]).update(occupied=spot["occupied"])

        self.pr_info["Occupancy"], self.pr_info["Available"] = fs, es

        annotator.display_analytics(im0, self.pr_info, (104, 31, 17), (255, 255, 255), 10)
        self.display_output(im0)  # display output with base class function
        return im0  # return output image for more usage

    def runParkingDetection(self, imagePath: str):
        managment = ParkingManagement(model_path = MODEL)
        managment.json = managment.loadCameraVertices(imagePath)
        imgBGR = cv2.imread(imagePath)

        if imgBGR is None:
            print(f"Could not open {imagePath}")
            return
        
        results = managment.model.track(imgBGR, persist = True, show = False)

        if results and results[0].boxes:
            output = managment.process_data(imgBGR)
            # cv2.imwrite(imagePath, output)
            # print("Saved img!!")

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
        
        print(camera.parking_spots.all())

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
        print(camera.parking_spots.all())

        # Run parking detection on the uploaded image
        image_path = new_image.image.path  # Get the path to the saved image
        parking_management = ParkingManagement(model_path='yolov8n.pt')
        parking_management.runParkingDetection(image_path)

        return JsonResponse({
            'message': 'Image uploaded successfully',
            'camera_id': camera.id,
            'new_image_url': new_image.image.url,
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)