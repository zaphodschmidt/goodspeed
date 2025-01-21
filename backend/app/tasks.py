import base64
from celery import shared_task
import cv2
import numpy as np
from io import BytesIO
from PIL import Image as PILImage
from app.services.parking_management import ParkingManagement

@shared_task
def run_parking_detection(image_content, image_name, cam_num, building_name):
    # Decode the image content
    image_data = base64.b64decode(image_content)
    image = np.array(PILImage.open(BytesIO(image_data)))

    # Initialize ParkingManagement
    parking_management = ParkingManagement(model_path='yolov8n.pt')

    # Generate a fake file path for logging (optional)
    image_path = f"/tmp/{image_name}"  # For reference or debugging

    # Process the image
    parking_management.runParkingDetection(image_content, building_name, cam_num)

    # Log success
    print(f"Processed image: {image_path} for camera {cam_num} in building {building_name}")
