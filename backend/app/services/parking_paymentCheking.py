import http.client
import base64
import json
import os

from dotenv import load_dotenv, find_dotenv
from app.models import ParkingSpot, Building
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

load_dotenv(find_dotenv())

PARKMOBILE_AVALON_USERNAME = os.environ.get("PARKMOBILE_AVALON_USERNAME")
PARKMOBILE_AVALON_PASSWORD = os.environ.get("PARKMOBILE_AVALON_PASSWORD")
PARKMOBILE_CAPI_USERNAME = os.environ.get("PARKMOBILE_CAPI_USERNAME")
PARKMOBILE_CAPI_PASSWORD = os.environ.get("PARKMOBILE_CAPI_PASSWORD")
PARKMOBILE_NY_USERNAME = os.environ.get("PARKMOBILE_NY_USERNAME")
PARKMOBILE_NY_PASSWORD = os.environ.get("PARKMOBILE_NY_PASSWORD")
PARKMOBILE_APIKEY = os.environ.get("PARKMOBILE_APIKEY")

def getAllParkinglots():
    login = {
        "avalon":(PARKMOBILE_AVALON_USERNAME, PARKMOBILE_AVALON_PASSWORD), 
        "capi":(PARKMOBILE_CAPI_USERNAME, PARKMOBILE_CAPI_PASSWORD), 
        "ny":(PARKMOBILE_NY_USERNAME, PARKMOBILE_NY_PASSWORD)
    }
    all_responses = []

    for user, pwd in login.items():
        credentials = f"{user}:{pwd}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        conn = http.client.HTTPSConnection("api.parkmobile.io")

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "x-api-key": PARKMOBILE_APIKEY
        }

        conn.request("GET", "/nforceapi/zones", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")

        try:
            parsed_data = json.loads(data)
            all_responses.append({
                "username": user,
                "status": res.status,
                "response": parsed_data
            })
        except json.JSONDecodeError:
            print(f"Failed to parse JSON for user {user}")
        
    return all_responses

class PaymentChecking():
    def __init__(self, username, password, api_key):
        self.username = username
        self.password = password
        self.api_key = api_key

    def get(self, endpoint):
        response = []
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
        conn = http.client.HTTPSConnection("api.parkmobile.io")

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "x-api-key": self.api_key
        }

        conn.request("GET", endpoint, headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")

        try:
            parsed_data = json.loads(data)
            response = {
                "response": parsed_data
            }
        except json.JSONDecodeError:
            print(f"Failed to parse JSON for user {self.username}")

        return response
    
    def getParking_Zone(self, zoneNumber:str):
        endpoint = f"/nforceapi/parkingrights/zone/{zoneNumber}?format=json"
        return self.get(endpoint)
    
    def getParking_Spot(self, zoneNumber:str, spotNumber:str):
        endpoint = f"/nforceapi/parkingrights/zone/{zoneNumber}/{spotNumber}?format=json"
        return self.get(endpoint)

    def getParking_SpotRange(self, zoneNumber:str, startSpotNumber:str, endSpotNumber:str):
        endpoint = f"/nforceapi/parkingrights/zone/{zoneNumber}/{startSpotNumber}/{endSpotNumber}?format=json"
        return self.get(endpoint)
        
    def getParking_LPN(self, LPN:str):
        endpoint = f"/nforceapi/parkingrights/vehicle/{LPN}?format=json"
        return self.get(endpoint)

    def checkOccupiedspot_building(self, building:str):
        pass

    #checks if all the occupied spots in a garage have been paid for
    def checkOccupiedspot_zone(self, buildingName:str, zoneNumber:str):
        occupiedSpots = (self.getParking_Zone(zoneNumber))['response']
        db_spots = []
        for spot in occupiedSpots["parkingRights"]:
            #If the building doesn't exist print and return
            try:
                building = Building.objects.get(name=buildingName)
            except Building.DoesNotExist:
                print(f"Building {building} does not exist!")
                # return
            
            #If the parking spot doesn't exist print and return
            try:
                parkingSpot = ParkingSpot.objects.filter(camera__building=building).filter(spot_num=spot["spaceNumber"])
                # if(parkingSpot.)
                print(parkingSpot)
                db_spots.append(parkingSpot)

            except ParkingSpot.DoesNotExist:
                print(f"Parking spot {spot["spaceNumber"]} does not exist!")
                # return
        return db_spots
        

if __name__ == "__main__":
    pay = PaymentChecking(PARKMOBILE_AVALON_USERNAME, PARKMOBILE_AVALON_PASSWORD, PARKMOBILE_APIKEY)
    pay.getParking_Zone("9163")
    pay.getParking_Spot("9163", "124")
    pay.getParking_SpotRange("9163", "100", "120")
    pay.getParking_LPN("39A98S")