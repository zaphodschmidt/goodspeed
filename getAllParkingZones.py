import http.client
import base64
import json

def getAllPakinglots():
    username1 = "ws_goodspeedavalon"
    password1 = "7rEBrA8t"

    username2 = "ws_goodspeedcapi"
    password2 = "x2warEya"

    username3 = "ws_goodspeedny"
    password3 = "yegItr6y"

    api_key = "f76e2c55-54ef-4d66-bce7-10bf6b61a059"
    login = [(username1, password1), (username2, password2), (username3, password3)]

    all_responses = []

    for user, pwd in login:
        credentials = f"{user}:{pwd}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

        conn = http.client.HTTPSConnection("api.parkmobile.io")

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "x-api-key": api_key
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

def getVertexParkingSpots(vertexZoneNum):
    allSpots = []

    user = "ws_goodspeedavalon"
    pwd = "7rEBrA8t"
    api_key = "f76e2c55-54ef-4d66-bce7-10bf6b61a059"

    credentials = f"{user}:{pwd}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    conn = http.client.HTTPSConnection("api.parkmobile.io")

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "x-api-key": api_key
    }

    conn.request("GET", f"/nforceapi/parkingrights/zone/{vertexZoneNum}?format=json", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    print(f"Status: {res.status}")
    print(f"Response: {data}")

    try:
        parsed_data = json.loads(data)
        allSpots.append({
            "username": user,
            "status": res.status,
            "response": parsed_data
        })
    except json.JSONDecodeError:
        print(f"Failed to parse JSON for user {user}")

    with open("allSpots.json", "w") as f:
        json.dump(allSpots, f, indent=4)

    print("All responses saved to allSpots.json")

getVertexParkingSpots("9163")