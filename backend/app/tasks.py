from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def run_parking_detection(image_path, cam_num, building_name):
    from .services.parking_detection import ParkingDetection
    parking_detection = ParkingDetection(model_path='yolov8n.pt')
    parking_detection.run_parking_detection(image_path, cam_num, building_name)
    logger.info(f"Spot detection completed for {image_path}")

