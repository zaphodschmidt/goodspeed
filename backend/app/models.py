from django.db import models
import pytz
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from datetime import datetime

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Building(models.Model):
    name = models.CharField(max_length=127)
    timezone = models.CharField(
        max_length=63,
        choices=[(tz, tz) for tz in pytz.common_timezones],
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
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='zones')

    def __str__(self):
        return f"Zone {self.zone_number} in spot {self.spt.name}"


class ParkingSpot(models.Model):
    spot_num = models.IntegerField()
    occupied = models.BooleanField(default=False) 
    start_datetime = models.DateTimeField(null=True) # start of parkmobile lease
    end_datetime = models.DateTimeField(null=True) # end of parkmobile lease
    occupied_by_lpn = models.CharField(null=True, max_length=15)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='parking_spots')
    zone = models.ForeignKey(Zone, null=True, on_delete=models.CASCADE, related_name='parking_spots')

    # class Meta:
    #     unique_together = ('spot_num', 'camera')

    def __str__(self):
        return f"Spot {self.spot_num} (Camera {self.camera.cam_num})"
    
    def save(self, *args, **kwargs):
        if self.zone and self.zone.building != self.camera.building:
            raise ValidationError(
                f"Zone {self.zone.zone_number} belongs to {self.zone.building.name}, "
                f"but this spot's camera is in {self.camera.building.name}. "
                "A zone cannot have parking spots from different buildings."
            )

        super().save(*args, **kwargs)
    

class Reservation(models.Model):
    spot = models.OneToOneField(ParkingSpot, related_name='reservation', on_delete=models.CASCADE)
    lpn = models.CharField(max_length=12)
    start_datetime = models.DateTimeField(default=now)
    end_datetime = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk and Reservation.objects.filter(spot=self.spot).exists():
            raise ValidationError(f"Parking spot {self.spot} is already reserved")

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        print(self.end_datetime)
        return now() > self.end_datetime


class Vertex(models.Model):
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name='vertices')
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f"Vertex ({self.x}, {self.y}) for Spot {self.spot.spot_num}"