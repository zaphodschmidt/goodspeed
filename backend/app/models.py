from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name

class Camera(models.Model):
    cam_num = models.IntegerField()
    garage = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='cameras')
    MAC = models.CharField(max_length=50, unique=True)
    IP = models.GenericIPAddressField()

    class Meta:
        unique_together = ('cam_num', 'garage')

    def __str__(self):
        return f"Camera {self.cam_num} in {self.garage.name}"
    
class ParkingSpot(models.Model):
    spot_num = models.IntegerField()
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='parking_spots')

    class Meta:
        unique_together = ('spot_num', 'camera')

    def __str__(self):
        return f"Spot {self.spot_num} (Camera {self.camera.cam_num})"

class Vertex(models.Model):
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name='vertices')
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f"Vertex ({self.x}, {self.y}) for Spot {self.spot.spot_num}"