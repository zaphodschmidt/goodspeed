from rest_framework.test import APITestCase
from rest_framework import status
from .models import Building, Camera, ParkingSpot, Vertex
from .serializers import ParkingSpotSerializer


class ParkingSpotSerializerTestCase(APITestCase):

    def setUp(self):
        # Create a Building and a Camera
        self.building = Building.objects.create(name="Test Building")
        self.camera = Camera.objects.create(
            cam_num=1, building=self.building, MAC="00:11:22:33:44:55", IP="192.168.0.1"
        )

    def test_create_parking_spot_with_default_vertices(self):
        # Data to create a parking spot
        data = {"spot_num": 1, "camera": self.camera.id, "vertices": []}

        # Serialize and save the parking spot
        serializer = ParkingSpotSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        parking_spot = serializer.save()

        # Check the parking spot is created
        self.assertEqual(ParkingSpot.objects.count(), 1)
        self.assertEqual(Vertex.objects.count(), 4)

        # Verify default vertices
        vertices = Vertex.objects.filter(spot=parking_spot)
        expected_positions = [
            {"x": 30, "y": 30},
            {"x": 70, "y": 30},
            {"x": 30, "y": 70},
            {"x": 70, "y": 70},
        ]
        actual_positions = [{"x": v.x, "y": v.y} for v in vertices]
        self.assertCountEqual(actual_positions, expected_positions)


def test_update_parking_spot_with_nested_vertices(self):
    # Create a parking spot
    parking_spot = ParkingSpot.objects.create(spot_num=1, camera=self.camera)

    # Create default vertices manually (mimicking create behavior)
    vertex1 = Vertex.objects.create(spot=parking_spot, x=30, y=30)
    vertex2 = Vertex.objects.create(spot=parking_spot, x=70, y=30)
    vertex3 = Vertex.objects.create(spot=parking_spot, x=30, y=70)
    vertex4 = Vertex.objects.create(spot=parking_spot, x=70, y=70)

    # Data to update parking spot with nested vertices
    data = {
        "spot_num": 1,
        "camera": self.camera.id,
        "vertices": [
            {"id": vertex1.id, "x": 40, "y": 40},  # Update first vertex
            {"id": vertex4.id, "x": 80, "y": 80},  # Update last vertex
        ],
    }

    # Serialize and update the parking spot
    serializer = ParkingSpotSerializer(parking_spot, data=data)
    self.assertTrue(
        serializer.is_valid(), serializer.errors
    )  # Include errors if validation fails
    serializer.save()

    # Verify vertices are updated
    updated_vertices = Vertex.objects.filter(spot=parking_spot)
    updated_positions = [{"x": v.x, "y": v.y} for v in updated_vertices]
    expected_positions = [
        {"x": 40, "y": 40},  # Updated position
        {"x": 70, "y": 30},  # Unchanged
        {"x": 30, "y": 70},  # Unchanged
        {"x": 80, "y": 80},  # Updated position
    ]
    self.assertCountEqual(updated_positions, expected_positions)
