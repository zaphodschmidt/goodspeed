from celery import shared_task
from app.services.parking_management import ParkingManagement

@shared_task
def run_parking_detection(image_path):
    parking_management = ParkingManagement(model_path='yolov8n.pt')
    parking_management.runParkingDetection(image_path)