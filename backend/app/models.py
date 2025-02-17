from django.db import models
from pytz import common_timezones
from storages.backends.s3boto3 import S3Boto3Storage


class Image(models.Model):
    image = models.ImageField(upload_to="images/", storage=S3Boto3Storage)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Building(models.Model):
    name = models.CharField(max_length=127)
    timezone = models.CharField(max_length=63, choices=[(tz, tz) for tz in common_timezones], default="UTC")

    def __str__(self):
        return self.name


class Camera(models.Model):
    cam_num = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="cameras")
    MAC = models.CharField(max_length=50, unique=True)
    IP = models.GenericIPAddressField()
    image = models.OneToOneField(Image, null=True, on_delete=models.SET_NULL, related_name="camera")

    class Meta:
        unique_together = ("cam_num", "building")

    def __str__(self):
        return f"Camera {self.cam_num} in {self.building.name}"


class SpotType(models.Model):
    """
    Defines the type of parking spot and how reservations work for it. 
    
    reservation_basis:
        - "per_spot": A reservation is tied to a specific spot.
        - "per_type": A reservation allows parking in any spot of this type.
        - "parkmobile": The spot is managed by ParkMobile.
        - "none": No reservations are allowed for this type.
    building: what building this spot type is for
    """
    RESERVATION_BASIS_CHOICES = [
        ("per_spot", "Per-spot"),
        ("per_type", "Per-type"),
        ("parkmobile", "ParkMobile"),
        ("none", "None"),
    ]
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    reservation_basis = models.CharField(max_length=50, choices=RESERVATION_BASIS_CHOICES)


class Zone(models.Model):
    """
    Parkmobile Zone number. Optional for spots
    """
    zone_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Zone {self.zone_number} in spot {self.spt.name}"


class ParkingSpot(models.Model):
    """
    Represents an individual parking spot.

    Fields:
        - spot_num: The spot number.
        - occupied: Whether the spot is currently occupied.
        - occupied_by_lpn: The license plate number (LPN) of the vehicle occupying the spot.
        - camera: The camera monitoring this spot.
        - type: The type/category of this spot.
    """
    spot_num = models.IntegerField()
    occupied = models.BooleanField(default=False)
    occupied_by_lpn = models.CharField(null=True, max_length=15)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name="parking_spots")
    type = models.ForeignKey(SpotType, null=True, on_delete=models.CASCADE, related_name="parking_spots")
    zone = models.ForeignKey(Zone, null=True, on_delete=models.CASCADE, related_name='parking_spots')

    def __str__(self):
        return f"Spot {self.spot_num} (Camera {self.camera.cam_num})"


class ReservationType(models.Model):
    """
    Defines the type of reservation and its constraints.

    Fields:
        - name: The name of the reservation type.
        - description: A text description of what this reservation type entails.
        - spot_type: Which categories of spot this reservation applies to. (many to many)
        - business_days: Whether the reservation is valid only on business days.
        - active_at: The time of day this reservation becomes active each day. Defaults to midnight.
        - inactive_at: The time of day this reservation becomes inactive each day. Defaults to 11:59 PM.
        - duration: Specifies whether the reservation lasts for a day or a month.
    """
    DURATION_CHOICES = [
        ("day", "Day"),
        ("month", "Month"),
    ]
    name = models.CharField(max_length=50)  
    description = models.TextField(blank=True)
    spot_type = models.ManyToManyField(SpotType)
    only_business_days = models.BooleanField()  
    active_at = models.TimeField(default="00:00")  
    inactive_at = models.TimeField(default="23:59")
    duration = models.CharField(max_length=50, choices=DURATION_CHOICES)  


class Reservation(models.Model):
    """
    Represents a specific reservation for a vehicle.

    Fields:
        - reservation_type: The type of reservation
        - spot: The specific spot assigned to this reservation, if applicable (null if reserved per type).
        - start_date: The date the reservation starts.
        - LPN: The license plate number (LPN) of the vehicle this reservation is for.
    """
    reservation_type = models.ForeignKey(ReservationType, on_delete=models.CASCADE, related_name="reservations")
    spot = models.ForeignKey(ParkingSpot, null=True, on_delete=models.CASCADE, related_name="reservations")
    start_date = models.DateField()
    LPN = models.CharField(max_length=15)


class Vertex(models.Model):
    spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name="vertices")
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f"Vertex ({self.x}, {self.y}) for Spot {self.spot.spot_num}"
