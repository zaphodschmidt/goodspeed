from django.core.management.base import BaseCommand
from data.HalleyRiseSpotTypes import (
    Retail,
    Residential,
    GuaranteedOfficeParking,
    BlockC,
    SharedParkingSpaces,
)

class Command(BaseCommand):
    help = "Create predefined SpotType objects for Halley Rise"

    def handle(self, *args, **kwargs):
        spot_types = [
            Retail,
            Residential,
            GuaranteedOfficeParking,
            BlockC,
            SharedParkingSpaces,
        ]

        for spot in spot_types:
            spot.create()
            self.stdout.write(self.style.SUCCESS(f'Successfully created or updated: {spot.name}'))
