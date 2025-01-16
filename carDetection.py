import os
from PIL import Image
import cv2
from ultralytics import solutions
from ultralytics.solutions.parking_management import ParkingManagement

# PATH = './camera_snapshot_20250114210012_cam11.jpeg'
PATH = './commercial-parking-lots.jpg'
MODEL = 'yolov8n.pt'
BOUNDING = './bounding_boxes.json'
IMG_SAVE = './wow1.jpeg'


def isJpeg(file_path):
    try:
        with Image.open(file_path) as img:
            return img.format == 'JPEG'
    except (IOError, OSError):
        return False

def getDirs(path: str):
    files = []
    for fileName in os.scandir(path):
        if fileName.is_file() and isJpeg(fileName):
            files.append(path+"/"+fileName.name)
    return files

def runParkingDetection(imagePath: str, boundingBox: str):
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

if __name__ == "__main__":
    runParkingDetection(PATH, BOUNDING)
    # solutions.ParkingPtsSelection()

