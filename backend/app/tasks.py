from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def run_parking_detection(cam_num, building_name):
    from .services.parking_management import ParkingManagement
    parking_management = ParkingManagement(model_path='yolov8n.pt')
    parking_management.run_parking_detection(cam_num, building_name)
    logger.info(f"Spot detection completed for {cam_num} in {building_name}")

