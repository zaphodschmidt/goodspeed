from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Building, Camera, ParkingSpot, Zone

class Command(BaseCommand):
    help = 'Update parking spots in Building 4 to zone 9163'

    def handle(self, *args, **kwargs):
        zone_9163, created = Zone.objects.get_or_create(zone_number='9163')
        building_4 = Building.objects.get(id=4)
        cameras_in_building_4 = Camera.objects.filter(building=building_4)
        parking_spots_to_update = ParkingSpot.objects.filter(camera__in=cameras_in_building_4)

        with transaction.atomic():
            parking_spots_to_update.update(zone=zone_9163)

        self.stdout.write(self.style.SUCCESS(f"Updated {parking_spots_to_update.count()} parking spots to zone 9163."))