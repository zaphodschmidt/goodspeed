from app.models import Building, SpotType


class HalleyRiseSpotType:
    name = None
    description = None
    reservation_basis = None

    @classmethod
    def create(cls):
        if cls.name and cls.description and cls.reservation_basis:
            SpotType.objects.get_or_create(
                name=cls.name,
                description=cls.description,
                building=Building.objects.get(name='Halley Rise'),
                reservation_basis=cls.reservation_basis,
            )

"""
Small Garage
"""
class Retail(HalleyRiseSpotType):
    name = 'Retail'
    description = 'These are ParkMobile spaces in the Halley Rise small garage.'
    reservation_basis = 'parkmobile'


class Residential(HalleyRiseSpotType):
    name = 'Residentail'
    description = 'Individually assigned spaces for residents in the small garage.'
    reservation_basis = 'per_spot'


"""
Large Garage
"""
class GuaranteedOfficeParking(HalleyRiseSpotType):
    name = 'Guaranteed Office Parking'
    description = '24/7 parking for office employees (pay per month) and visitors (reserve per day at kiosk.)'
    reservation_basis = 'per_type'


class BlockC(HalleyRiseSpotType):
    name = 'Block C'
    description = 'Spaces for residents in Halley Rise large building. Spots are reserved per month via premium subscription.'
    reservation_basis = 'per_spot'


class SharedParkingSpaces(HalleyRiseSpotType):
    name = 'Shared Parking Spaces'
    description = 'Spaces shared by residents with base subscription and office parkers, paid on a monthly basis.'
    reservation_basis = 'per_type'