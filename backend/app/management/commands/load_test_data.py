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

                # Create parking spots for the cameras
                # Assign spots 1,2 to Camera 2 and 3,4 to Camera 3
                start_spot_num = (cam_index - 2) * 2 + 1
                for spot_index in range(start_spot_num, start_spot_num + 2):
                    spot = ParkingSpot.objects.create(
                        spot_num=spot_index, camera=camera
                    )
                    self.stdout.write(
                        f"    Created: Spot {spot.spot_num} for Camera {camera.cam_num}"
                    )

                    # Create vertices for each parking spot
                    vertices = [
                        (10 * spot_index, 20 * spot_index),
                        (10 * spot_index + 10, 20 * spot_index),
                        (10 * spot_index + 10, 20 * spot_index + 10),
                        (10 * spot_index, 20 * spot_index + 10),
                    ]
                    for x, y in vertices:
                        vertex = Vertex.objects.create(spot=spot, x=x, y=y)
                        self.stdout.write(
                            f"      Created: Vertex ({vertex.x}, {vertex.y}) for Spot {spot.spot_num}"
                        )

        self.stdout.write(self.style.SUCCESS("Database populated with dummy data!"))
