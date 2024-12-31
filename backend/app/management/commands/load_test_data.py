from django.core.management.base import BaseCommand
from app.models import Building, Camera, ParkingSpot, Vertex


class Command(BaseCommand):
    help = "Populates the database with dummy test data"

    def handle(self, *args, **kwargs):
        # Clear existing data
        Vertex.objects.all().delete()
        ParkingSpot.objects.all().delete()
        Camera.objects.all().delete()
        Building.objects.all().delete()

        # Create buildings
        for building_index in range(1, 3):  # Two buildings
            building = Building.objects.create(name=f"Building {building_index}")
            self.stdout.write(f"Created: {building.name}")

            # Create cameras for each building
            for cam_index in range(2, 4):  # Two cameras per building
                camera = Camera.objects.create(
                    cam_num=cam_index,
                    building=building,
                    MAC=f"EC:71:DB:{building_index:02}:{cam_index:02}:{building_index + cam_index:02}",
                    IP=f"192.168.{building_index}.{cam_index}",
                )
                self.stdout.write(
                    f"  Created: Camera {camera.cam_num} in {building.name}"
                )

        self.stdout.write(self.style.SUCCESS("Database populated with dummy data!"))
