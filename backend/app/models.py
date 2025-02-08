from django.db import models
from pytz import common_timezones

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Building(models.Model):
    name = models.CharField(max_length=127)
    timezone = models.CharField(
        max_length=63,
        choices=[(tz, tz) for tz in common_timezones],
        default='UTC'
    )

    def __str__(self):
        return self.name

class Camera(models.Model):
    cam_num = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='cameras')
    MAC = models.CharField(max_length=50, unique=True)
    IP = models.GenericIPAddressField()
    image = models.OneToOneField(Image, null=True, on_delete=models.SET_NULL, related_name='camera')

    class Meta:
        unique_together = ('cam_num', 'building')

    def __str__(self):
        return f"Camera {self.cam_num} in {self.building.name}"

class Zone(models.Model):
    zone_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Zone {self.zone_number} in spot {self.spt.name}"

class ParkingSpot(models.Model):
    spot_num = models.IntegerField()
    occupied = models.BooleanField(default=False) 
    start_datetime = models.DateTimeField(null=True) # start of parkmobile lease
    end_datetime = models.DateTimeField(null=True) # end of parkmobile lease
    reserved_by_lpn = models.CharField(null=True, max_length=15)
    occupied_by_lpn = models.CharField(null=True, max_length=15)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='parking_spots')
    zone = models.ForeignKey(Zone, null=True, on_delete=models.CASCADE, related_name='parking_spots')

    # class Meta:
    #     unique_together = ('spot_num', 'camera')

    def __str__(self):
        return f"Spot {self.spot_num} (Camera {self.camera.cam_num})"

class Vertex(models.Model):
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name='vertices')
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f"Vertex ({self.x}, {self.y}) for Spot {self.spot.spot_num}"