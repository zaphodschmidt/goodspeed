from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from app.models import ParkingSpot, Building, Camera, Location
from app.serializers import ParkingSpotSerializer

class LocationHandler:
    def __init__(self, building_id:int):
        self.building_id = building_id
        
    def addLocationToCamera(self, location:str, camera_id: int):
        buildingObj = get_object_or_404(Building, id=self.building_id)
        location = get_object_or_404(Location, name=location)

        try:
            camera = Camera.objects.get(id=camera_id, building=buildingObj)
            camera.location = location
            camera.save()
        except Camera.DoesNotExist:
            print(f"Camera with ID {camera_id} does not exist in building {buildingObj.name}.")
    
    def getOccupancyForLocation(self, location:str):
        buildingObj = get_object_or_404(Building, id=self.building_id)
        cameras = Camera.objects.filter(building = buildingObj)

        try:
            cameras = Camera.objects.filter(building = buildingObj)
            cameras = Camera.objects.filter(location = location)
        except Exception as e:
            print(f"Error: Cameras could not be found \n {e}!")
            raise

        try:
            parkingSpots = ParkingSpot.objects.filter(camera__in = cameras)
            parkingSpots = ParkingSpotSerializer(parkingSpots, many=True).data
            parkingSpots = {spot['spot_num']: spot for spot in parkingSpots}
        except Exception as e:
            print(f"Error: Parking Spots could not be found \n {e}!")
            raise

        occupiedSpots = 0
        totalSpots = 0
        for _, spotObj in parkingSpots.items():
            if spotObj['occupied']:
                occupiedSpots+=1
            totalSpots+=1

        return JsonResponse({
            'location':location,
            'totalSpots': totalSpots,
            'occupiedSpots': occupiedSpots
        })