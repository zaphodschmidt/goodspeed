import os
from PIL import Image as PILImage
import cv2
import numpy as np
from ultralytics.solutions.solutions import BaseSolution, YOLO
from app.models import Building, Camera, ParkingSpot
from django.db import transaction
from app.serializers import VertexSerializer, ParkingSpotSerializer
import easyocr
import re
import requests
from pprint import pprint
from dotenv import load_dotenv, find_dotenv
from icecream import install, ic
install()
load_dotenv(find_dotenv())

MODEL = 'yolov8n.pt'
LPR_MODEL = 'best_model_NPT.pt'

class ParkingManagement(BaseSolution):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.json = None
        self.pr_info = {"Occupancy": 0, "Available": 0}
        self.arc = (0, 0, 255)
        self.occ = (0, 255, 0)
        self.dc = (255, 0, 189)
        self.spot_ids = []
        self.camera_obj = None
    
######################
######################
######################

    def load_camera_vertices(self, cam_num, building_name):
        # Find the Camera
        try:
            self.camera_obj = Camera.objects.get(cam_num=cam_num, building__name=building_name)
        except Camera.DoesNotExist:
            print(f"Camera {cam_num} does not exist in building {building_name}")
            return

        #assemble list of dictionaries of parking spot vertices.
        parking_spot_bounds = []
        for spot in self.camera_obj.parking_spots.all():
            if not spot.vertices.exists():
                print(f"Parking spot {spot.id} has no vertices.")
            else:
                points_dict = {"points": []}
                for point in spot.vertices.all():
                    points_dict["points"].append([point.x, point.y])
                parking_spot_bounds.append(points_dict)
                self.spot_ids.append(spot.id)

        return parking_spot_bounds
    
######################
######################
######################

    def process_data(self, im0):
        if not self.json:
            print("No parking spot data loaded.")
            return im0

        self.extract_tracks(im0)  # extract tracks from im0
        es, fs = len(self.json), 0  # empty slots, filled slots
        parking_spots_to_update = []
        for region , spot_id in zip(self.json, self.spot_ids):
            # Convert points to a NumPy array with the correct dtype and reshape properly
            pts_array = np.array(region["points"], dtype=np.int32).reshape((-1, 1, 2))
            rg_occupied = False  # occupied region initialization
            for box, cls in zip(self.boxes, self.clss):
                xc, yc = int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)
                dist = cv2.pointPolygonTest(pts_array, (xc, yc), False)
                if dist >= 0:
                    rg_occupied = True
                    break
            fs, es = (fs + 1, es - 1) if rg_occupied else (fs, es)
            # Plotting regions
            cv2.polylines(im0, [pts_array], isClosed=True, color=self.occ if rg_occupied else self.arc, thickness=2)
            parking_spots_to_update.append({"spot_id": spot_id, "occupied": rg_occupied})


        with transaction.atomic():
            for spot in parking_spots_to_update:
                ParkingSpot.objects.filter(id=spot["spot_id"]).update(occupied=spot["occupied"])
        self.pr_info["Occupancy"], self.pr_info["Available"] = fs, es
        self.display_output(im0)  # display output with base class function
        return im0  # return output image for more usage
    
######################
######################
######################
   
    def runLPDetection(self, img0):
        model = YOLO(LPR_MODEL)
        results = model.predict(img0)

        foundLPs = results[0].boxes.data.tolist()
        return foundLPs
    
######################
######################
######################

    def is_point_in_polygon(self, point, polygon):
        x, y = point['x'], point['y']
        inside = False
        n = len(polygon)

        p1 = polygon[0]
        for i in range(1, n + 1):
            p2 = polygon[i % n]
            if y > min(p1['y'], p2['y']):
                if y <= max(p1['y'], p2['y']):
                    if x <= max(p1['x'], p2['x']):
                        if p1['y'] != p2['y']:
                            xinters = (y - p1['y']) * (p2['x'] - p1['x']) / (p2['y'] - p1['y']) + p1['x']
                        else:
                            xinters = p1['x']
                        if p1['x'] == p2['x'] or x <= xinters:
                            inside = not inside
            p1 = p2

        return inside

    def LP_in_spot(self, lp, spot_polygon):
        x1, y1, x2, y2, conf, cls_id = lp
        poly_min_x = min(p['x'] for p in spot_polygon)
        poly_max_x = max(p['x'] for p in spot_polygon)
        poly_min_y = min(p['y'] for p in spot_polygon)
        poly_max_y = max(p['y'] for p in spot_polygon)

        if x1 < poly_min_x or x2 > poly_max_x or y1 < poly_min_y or y2 > poly_max_y:
            return False

        corners = [
            {'x': x1, 'y': y1},
            {'x': x2, 'y': y1},
            {'x': x2, 'y': y2},
            {'x': x1, 'y': y2}
        ]
        for corner in corners:
            if self.is_point_in_polygon(corner, spot_polygon):
                return True
        return False

    def LPR_connectPlatesToSpots(self, img0, foundLPs):
        spotsToLPs = {}
        #go through all the found license plates for the camera
        for spot in self.camera_obj.parking_spots.all():
            spot = ParkingSpotSerializer(spot).data
            if spot['occupied']:
                lps = []
                for lp in foundLPs:
                    if self.LP_in_spot(lp, spot['vertices']):
                        lps.append(lp)

                lenLps = len(lps)
                bestLP = None
                if lenLps<1:
                    continue

                elif lenLps == 1:
                    bestLP = lps[0]

                elif lenLps > 1:
                    mostAccurateScore = -1
                    bestLP = lps[0]
                    for lp in lps:
                        x1, y1, x2, y2, conf, cls_id = lp
                        if max(mostAccurateScore, conf) == conf:
                            mostAccurateScore = conf
                            bestLP = lp
                spotsToLPs[spot["id"]] = {"LP_bounding_box":bestLP}
        return spotsToLPs
    
######################
######################
######################

    def drawLP_polylines(self, img0, spotsToLPs:dict):
        for lp in spotsToLPs.values():
            x1, y1, x2, y2, conf, cls_id = lp["LP_bounding_box"]
            cv2.rectangle(img0, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
        return img0
    
######################
######################
######################

    def LP_encodeCroppedLPs(self, img0, lp:dict):
        x1, y1, x2, y2, conf, cls_id = lp["LP_bounding_box"]
        cropped_image = img0[int(y1):int(y2), int(x1):int(x2)]
        _, encodedImg = cv2.imencode('.jpg',cropped_image)
        imgBytes = encodedImg.tobytes()
        files = {
            'upload':('image.jpg', imgBytes, 'image/jpeg')
        }
        return files
    
    def LP_OCR(self, img0, spotsToLPs:dict):
        api_token = os.environ.get("OCR_API_TOKEN")
        regions = ["mx", "us-ca"] # Change to your country
        for spotNum, lp in spotsToLPs.items():
            files = self.LP_encodeCroppedLPs(img0, lp)
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),
                files=files,
                headers={'Authorization': f'Token {api_token}'},
                timeout = 10
            )
            
            pprint(response.json())
            spotsToLPs[spotNum]["LP_num"] = "HI"

######################
######################
######################

    def LP_inputDataToDB(self, spotsToLPs):
        pass

######################
######################
######################

    def run_parking_detection(self, image_path: str, cam_num: str, building_name:str):
        self.json = self.load_camera_vertices(cam_num=cam_num, building_name=building_name)
        imgBGR = cv2.imread(image_path)
        if imgBGR is None:
            print(f"Could not open {image_path}")
            return

        results = self.model.track(imgBGR, persist = True, show = False)
        if results and results[0].boxes:
            #Find car objects and determine if a spot is full or not
            car_occupancy_img = self.process_data(imgBGR)

            # #Find License plate bounding box
            foundLPs = self.runLPDetection(car_occupancy_img)

            #determine which license plate goes to which spot
            spotsToLPs = self.LPR_connectPlatesToSpots(car_occupancy_img, foundLPs)

            #draw license plate outline
            car_img_with_lps = self.drawLP_polylines(car_occupancy_img, spotsToLPs)

            #ocr the license plate text
            spotsToLPs = self.LP_OCR(car_img_with_lps, spotsToLPs)

            #Inputs complete licence plate location, text and spot it belongs to into the db
            self.LP_inputDataToDB(spotsToLPs)

            cv2.imwrite(image_path, car_img_with_lps)
            print("Saved img!!")