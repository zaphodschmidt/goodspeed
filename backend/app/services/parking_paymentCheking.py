import http.client
import base64
import json
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv, find_dotenv
from app.models import ParkingSpot, Building, Zone
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from app.serializers import ParkingSpotSerializer

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

    def get(self, endpoint:str):
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
    
    #TODO Finish email finding part of code
    def sendEmailForTicket(self, receiverEmail:str, building:str, spot:str):
        sender_email = "szaphod@gmail.com"
        receiverEmail ="parkerjeanneallen@gmail.com"
        # receiver_email ="zapschmidt@hotmail.com"
        password = "wovw qiay gkbo ylfv"
        subject = "Fuck you"
        body = "This is from a python script that I made :) I love you"

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiverEmail
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            server.quit()
    
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
        ##Get parking data from the DB
        #If the building doesn't exist print and return
        try:
            building = Building.objects.get(name=buildingName)
        except Building.DoesNotExist:
            print(f"Building {building} does not exist!")
            return
        
        #If the parking spot doesn't exist print and return
        try:
            parkingSpots = ParkingSpot.objects.filter(camera__building=building, zone__in=zoneNumber)
            jsonParkingSpots = ParkingSpotSerializer(parkingSpots, many=True).data

        except Zone.DoesNotExist:
            print(f"Parking spot {zoneNumber} does not exist!")
            return
                
        ##Get park mobile data
        occupiedSpots = (self.getParking_Zone(zoneNumber))['response']['parkingRights']
        prkmob_spots = {}
        for spot in occupiedSpots:
            prkmob_spots[spot["spaceNumber"]] = spot
        
        ##find who didn't pay
        for db_spot in jsonParkingSpots:
            #if the spot is occupied and they didn't pay their ticket
            if db_spot['occupied'] and db_spot["spot_num"] not in prkmob_spots["spaceNumber"]:
                #TODO send text to person
                pass

if __name__ == "__main__":
    pay = PaymentChecking(PARKMOBILE_AVALON_USERNAME, PARKMOBILE_AVALON_PASSWORD, PARKMOBILE_APIKEY)
    pay.getParking_Zone("9163")
    pay.getParking_Spot("9163", "124")
    pay.getParking_SpotRange("9163", "100", "120")
    pay.getParking_LPN("39A98S")