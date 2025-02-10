import os
from PIL import Image as PILImage
import cv2
import numpy as np
from ultralytics.solutions.solutions import BaseSolution, YOLO
from app.models import Building, Camera, ParkingSpot
from django.db import transaction
from app.serializers import VertexSerializer, ParkingSpotSerializer

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
        self.normalImgW = 2560
        self.normalImgH = 1920
        self.webpageImgW = 1000
        self.webpageImgH = 750
        self.buildingName = None
        self.cameraNum = None
        self.cameraObj = None
        
    def loadCameraVertices(self, photo: str):
        # Extract building name and camera number from the filename
        self.buildingName = photo.split('_')[3]
        cameraNumStr = photo.split('_')[4]  # This will be "cam11.jpeg"
        self.cameraNum = int(cameraNumStr[3:].split('.')[0])  # Remove "cam" and ".jpeg"
        
        if self.buildingName.lower() == "vertex1":
            buildingName = "Vertex"
        try:
            building = Building.objects.get(name=buildingName)
        except Building.DoesNotExist:
            print(f"Building '{buildingName}' does not exist.")
            return
        try:
            self.cameraObj = building.cameras.get(cam_num=self.cameraNum)
        except Camera.DoesNotExist:
            print(f"Camera {self.cameraNum} does not exist in building {building.name}.")
            return
        #calc how much the boudning boxes need to be scaled
        scaleW = self.normalImgW / self.webpageImgW
        scaleH = self.normalImgH / self.webpageImgH
        parkingSpotBounds = []
        self.spot_ids = []
        for spot in self.cameraObj.parking_spots.all():
            print(f"Found parking spot: {spot}")
            if not spot.vertices.exists():
                print(f"Parking spot {spot.id} has no vertices.")
            else:
                pointsDict = {"points": []}
                for point in spot.vertices.all():
                    pointsDict["points"].append([point.x * scaleW, point.y * scaleH])
                parkingSpotBounds.append(pointsDict)
                self.spot_ids.append(spot.id)

        print(f"Loaded parking spots: {self.spot_ids}")
        return parkingSpotBounds

    def isJpeg(self, file_path:str):
        try:
            with PILImage.open(file_path) as img:
                return img.format == 'JPEG'
        except (IOError, OSError):
            return False

    def getDirs(self, path: str):
        files = []
        for fileName in os.scandir(path):
            if fileName.is_file() and self.isJpeg(fileName):
                files.append(path+"/"+fileName.name)
        return files
    
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
    
    def drawLP_polylines(self, img0, lp):
        x1, y1, x2, y2, id, score,label = lp
        cv2.rectangle(img0, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
        pts = np.array([
            [int(x1), int(y1)],
            [int(x2), int(y1)],
            [int(x2), int(y2)],
            [int(x1), int(y2)]
        ], np.int32)
        
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img0, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

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
        print(f"QOWL: {spot_polygon}")
        print([p['x'] for p in spot_polygon])
        print([p['y'] for p in spot_polygon])


        x1, y1, x2, y2, obj_id, score, label = lp
        print(f"x1 :{x1}, y1 {y1}, x2: {x2}, y2:{y2}")
        poly_min_x = min(p['x'] for p in spot_polygon)
        poly_max_x = max(p['x'] for p in spot_polygon)
        poly_min_y = min(p['y'] for p in spot_polygon)
        poly_max_y = max(p['y'] for p in spot_polygon)
        
        if x1 < poly_min_x or x2 > poly_max_x or y1 < poly_min_y or y2 > poly_max_y:
            print("RETURNED FALSE")
            return False
        print("RETURNED TRUE")

        corners = [
            {'x': x1, 'y': y1},
            {'x': x2, 'y': y1},
            {'x': x2, 'y': y2},
            {'x': x1, 'y': y2}
        ]
        for corner in corners:
            if self.is_point_in_polygon(corner, spot_polygon):
                print(f"LICENSE PLATE THAT IS IN A SPOT: {lp}")
                return True
        print(f"NO LP IN SPOT: {spot_polygon['']}")
        return False

    def runLPDetection(self, img0):
        model = YOLO(LPR_MODEL)
        results = model.track(img0,persist=True)
        foundLPs = results[0].boxes.data.tolist()

        #go through all the found license plates for the camera
        for spot in self.cameraObj.parking_spots.all():
            spot = ParkingSpotSerializer(spot).data
            if spot['occupied']:
                print("###################################################################")
                print(spot)
                lps = []
                for i, lp in enumerate(foundLPs):
                    if self.LP_in_spot(lp, spot['vertices']):
                        lps.append([i,lp])

                for i in lps:
                    foundLPs.remove(lps[i])

                lenLps = len(lps)
                bestLP = None
                if lenLps<1:
                    print("DID NOT FIND LP IN OCCUPIED SPOT!!!!!!!!")
                    continue
                elif lenLps > 1:
                    mostAccurateScore = -1
                    bestLP = lps[0][1]
                    print(bestLP)
                    for i in range(1,lenLps-1):
                        print(f"LPS: {lps[i]}")
                        x1, y1, x2, y2, obj_id, score, label = lps[i][1]
                        if max(mostAccurateScore, score) == score:
                            mostAccurateScore = score
                            bestLP = lps[i][1]

                #draw line and do analysis
                print(bestLP)
                self.drawLP_polylines(img0, bestLP)

        return img0

    def runParkingDetection(self, imagePath: str):
        self.json = self.loadCameraVertices(imagePath)
        imgBGR = cv2.imread(imagePath)
        if imgBGR is None:
            print(f"Could not open {imagePath}")
            return
        
        results = self.model.track(imgBGR, persist = True, show = False)
        if results and results[0].boxes:
            carOccupancy = self.process_data(imgBGR)
            carLPs = self.runLPDetection(carOccupancy)

            cv2.imwrite(imagePath, carLPs)
            print("Saved img!!")