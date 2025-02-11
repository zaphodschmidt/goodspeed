# parking/management/commands/detect_parking.py
from django.core.management.base import BaseCommand
import os
from app.tasks import run_parking_detection

class Command(BaseCommand):
    help = 'Detect parking in an image'

    def add_arguments(self, parser):
        # Add the image path argument
        parser.add_argument('image_path', type=str, help='Path to the image for parking detection')
        parser.add_argument('cam_num', type=str, help='Camera number')
        parser.add_argument('building_name', type=str, help='Name of building')

    def handle(self, *args, **options):
        # Get the image path from the command line argument
        image_path = options['image_path']
        cam_num = options['cam_num']
        building_name = options['building_name']
        if os.path.exists(image_path):
            self.stdout.write(f"Running parking detection on image: {image_path}")
            run_parking_detection.delay(image_path, cam_num, building_name)  
        else:
            self.stderr.write(f"Error: The image path '{image_path}' does not exist.")
