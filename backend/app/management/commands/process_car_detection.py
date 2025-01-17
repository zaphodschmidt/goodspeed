import os
from PIL import Image
import cv2
import numpy as np
import json
from ultralytics import solutions
from ultralytics.solutions.solutions import BaseSolution
from ultralytics.utils import LOGGER
from ultralytics.utils.checks import check_requirements
from ultralytics.utils.plotting import Annotator
from app.models import Building, Camera, ParkingSpot, Vertex
from django.core.management.base import BaseCommand

PATH = '/Users/zaphodschmidt/Desktop/coding/goodspeed/backend/media/uploads/camera_snapshot_20250116222005_vertex1_cam6.jpeg'
MODEL = 'yolov8n.pt'
IMG_SAVE = './wow1.jpeg'
BOUNDING = './bounding_boxes.json'

class ParkingManagement(BaseSolution):
    """
    Manages parking occupancy and availability using YOLO model for real-time monitoring and visualization.

    This class extends BaseSolution to provide functionality for parking lot management, including detection of
    occupied spaces, visualization of parking regions, and display of occupancy statistics.

    Attributes:
        json_file (str): Path to the JSON file containing parking region details.
        json (List[Dict]): Loaded JSON data containing parking region information.
        pr_info (Dict[str, int]): Dictionary storing parking information (Occupancy and Available spaces).
        arc (Tuple[int, int, int]): RGB color tuple for available region visualization.
        occ (Tuple[int, int, int]): RGB color tuple for occupied region visualization.
        dc (Tuple[int, int, int]): RGB color tuple for centroid visualization of detected objects.

    Methods:
        process_data: Processes model data for parking lot management and visualization.

    Examples:
        >>> from ultralytics.solutions import ParkingManagement
        >>> parking_manager = ParkingManagement(model="yolov8n.pt", json_file="parking_regions.json")
        >>> print(f"Occupied spaces: {parking_manager.pr_info['Occupancy']}")
        >>> print(f"Available spaces: {parking_manager.pr_info['Available']}")
    """

    def __init__(self, **kwargs):
        """Initializes the parking management system with a YOLO model and visualization settings."""
        super().__init__(**kwargs)

        self.pr_info = {"Occupancy": 0, "Available": 0}  # dictionary for parking information

        self.arc = (0, 0, 255)  # available region color
        self.occ = (0, 255, 0)  # occupied region color
        self.dc = (255, 0, 189)  # centroid color for each box
    
    def loadCameraVertecies(self, photo: str):
        buildingName = photo.split('_')[3]
        cameraNum = int(photo.split('_')[4][3])
        print(f"Bulding = {buildingName}")
        print(f"Camera# = {cameraNum}")

        if buildingName.lower() == "vertex1":
            buildingName = "Vertex"
        # cameraNum = f"Camera {cameraNum} in Vertex"

        try:
            building = Building.objects.get(name=buildingName)
        except Building.DoesNotExist:
            print(f"Building '{buildingName}' does not exist.")
            return

        print(f"Cameras in {building.name}: {building.cameras.all()}")

        try:
            camera = building.cameras.get(cam_num=cameraNum)
        except Camera.DoesNotExist:
            print(f"Camera {cameraNum} does not exist in building {building.name}.")
            return
        
        print(f"Spots in {camera.cam_num} : {camera.parking_spots.all()}")

        # try:
            

    def isJpeg(self, file_path:str):
        try:
            with Image.open(file_path) as img:
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
        """
        Processes the model data for parking lot management.

        This function analyzes the input image, extracts tracks, and determines the occupancy status of parking
        regions defined in the JSON file. It annotates the image with occupied and available parking spots,
        and updates the parking information.

        Args:
            im0 (np.ndarray): The input inference image.

        Examples:
            >>> parking_manager = ParkingManagement(json_file="parking_regions.json")
            >>> image = cv2.imread("parking_lot.jpg")
            >>> parking_manager.process_data(image)
        """

        self.extract_tracks(im0)  # extract tracks from im0
        es, fs = len(self.json), 0  # empty slots, filled slots
        print(f"JSON_FILE: {self.json_file}")
        annotator = Annotator(im0, self.line_width)  # init annotator

        for region in self.json:
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

        self.pr_info["Occupancy"], self.pr_info["Available"] = fs, es

        annotator.display_analytics(im0, self.pr_info, (104, 31, 17), (255, 255, 255), 10)
        self.display_output(im0)  # display output with base class function
        return im0  # return output image for more usage

    def runParkingDetection(self, imagePath: str, boundingBox: str):
        managment = ParkingManagement(model_path = MODEL, json_file = boundingBox)
        imgBGR = cv2.imread(imagePath)

        if imgBGR is None:
            print(f"Could not open {imagePath}")
            return
        
        results = managment.model.track(imgBGR, persist = True, show = False)

        if results and results[0].boxes:
            output = managment.process_data(imgBGR)
            cv2.imwrite(IMG_SAVE, output)
            print("Saved img!!")

class Command(BaseCommand):
    help = "Detects where the cars are in the parking lot"

    def handle(self, *args, **kwargs):
        parking = ParkingManagement(model_path = MODEL, json_file = BOUNDING)
        # parking.runParkingDetection(PATH, BOUNDING)
        parking.loadCameraVertecies(PATH)
        # solutions.ParkingPtsSelection()