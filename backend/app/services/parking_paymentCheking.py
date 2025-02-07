import http.client
import base64
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

PARKMOBILE_AVALON_USERNAME = os.environ.get("PARKMOBILE_AVALON_USERNAME")
PARKMOBILE_AVALON_PASSWORD = os.environ.get("PARKMOBILE_AVALON_PASSWORD")
PARKMOBILE_CAPI_USERNAME = os.environ.get("PARKMOBILE_CAPI_USERNAME")
PARKMOBILE_CAPI_PASSWORD = os.environ.get("PARKMOBILE_CAPI_PASSWORD")
PARKMOBILE_NY_USERNAME = os.environ.get("PARKMOBILE_NY_USERNAME")
PARKMOBILE_NY_PASSWORD = os.environ.get("PARKMOBILE_NY_PASSWORD")
PARKMOBILE_APIKEY = os.environ.get("PARKMOBILE_APIKEY")

def getAllPakinglots():
    login = {
        "avalon":(PARKMOBILE_AVALON_USERNAME, PARKMOBILE_AVALON_PASSWORD), 
        "avalon":(PARKMOBILE_CAPI_USERNAME, PARKMOBILE_CAPI_PASSWORD), 
        "avalon":(PARKMOBILE_NY_USERNAME, PARKMOBILE_NY_PASSWORD)
    }
    all_responses = []

    for user, pwd in login:
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

        print(f"Status: {res.status}")
        print(f"Response: {data}")

        try:
            parsed_data = json.loads(data)
            all_responses.append({
                "username": user,
                "status": res.status,
                "response": parsed_data
            })
        except json.JSONDecodeError:
            print(f"Failed to parse JSON for user {user}")

    with open("response.json", "w") as f:
        json.dump(all_responses, f, indent=4)

    print("All responses saved to all_responses.json")

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

        print(f"Status: {res.status}")
        print(f"Response: {data}")

        try:
            parsed_data = json.loads(data)
            response = {
                "response": parsed_data
            }
        except json.JSONDecodeError:
            print(f"Failed to parse JSON for user {self.username}")

        with open("allSpots.json", "w") as f:
            json.dump(response, f, indent=4)
            print("All responses saved to allSpots.json")

        return response
    
    def getParking_Zone(self, zoneNumber:str):
        endpoint = f"/nforceapi/parkingrights/zone/{zoneNumber}?format=json"
        self.get(endpoint)
    
    def getParking_Spot(self, zoneNumber:str, spotNumber:str):
        endpoint = f"/nforceapi/parkingrights/zone/{zoneNumber}/{spotNumber}?format=json"
        self.get(endpoint)

    def getParking_SpotRange(self, zoneNumber:str, startSpotNumber:str, endSpotNumber:str):
        endpoint = f"/nforceapi/parkingrights/zone/{zoneNumber}/{startSpotNumber}/{endSpotNumber}?format=json"
        self.get(endpoint)
        
    def getParking_LPN(self, LPN:str):
        endpoint = f"/nforceapi/parkingrights/vehicle/{LPN}?format=json"
        self.get(endpoint)

if __name__ == "__main__":
    pay = PaymentChecking(PARKMOBILE_AVALON_USERNAME, PARKMOBILE_AVALON_PASSWORD, PARKMOBILE_APIKEY)
    pay.getParking_Zone("9163")
    pay.getParking_Spot("9163", "124")
    pay.getParking_SpotRange("9163", "100", "120")
    pay.getParking_LPN("39A98S")
