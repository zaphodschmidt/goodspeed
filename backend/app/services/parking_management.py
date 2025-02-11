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

MODEL = 'yolov8n.pt'
LPR_MODEL = 'best_model_NPT.pt'

class ZapsOCR():
    def __init__(self) -> None:
        pass

    def noiseRemova(self, image):
        import numpy as np
        kernel = np.ones((1,1), np.uint8)
        image = cv2.dilate(image, kernel, iterations=1)
        kernel = np.ones((1,1),np.uint8)
        image = cv2.erode(image, kernel, iterations=1)

        # #Gets rid of noise
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        image = cv2.medianBlur(image,3)
        return image

    def thinFont(self, image):
        import numpy as np
        image = cv2.bitwise_not(image)
        #maks thinner
        kernel = np.ones((2,2), np.uint8)
        image = cv2.erode(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return image

    def thickFont(self, image):
        import numpy as np
        image = cv2.bitwise_not(image)
        kernel = np.ones((1,1), np.uint8)
        #maks thicker
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.bitwise_not(image)
        return image

    def getSkewAngle(cvImage) -> float:
        # Prep image, copy, convert to gray scale, blur, and threshold
        newImage = cvImage.copy()
        gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Apply dilate to merge text into meaningful lines/paragraphs.
        # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
        # But use smaller kernel on Y axis to separate between different blocks of text
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
        dilate = cv2.dilate(thresh, kernel, iterations=5)

        # Find all contours
        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)

        # Find largest contour and surround in min area box
        largestContour = contours[0]
        minAreaRect = cv2.minAreaRect(largestContour)

        # Determine the angle. Convert it to the value that was originally used to obtain skewed image
        angle = minAreaRect[-1]
        if angle < -45:
            angle = 90 + angle
        return -1.0 * angle

    # Rotate the image around its center
    def rotateImage(self, cvImage, angle:float):
        newImage = cvImage.copy()
        (h, w) = newImage.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return newImage

    # Deskew image
    def deskew(self, cvImage):
        angle = self.getSkewAngle(cvImage)
        return self.rotateImage(cvImage, -1.0 * angle)

    def removeBorder(self, image):
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cntSorted = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
        cnt = cntSorted[0]
        x, y, w, h = cv2.boundingRect(cnt)
        crop = image[y:y+h, x:x+w]
        return crop

    def analyzeLP(self, img0, bestLP, debug=True):
        x1, y1, x2, y2, conf, cls_id = bestLP
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        lp = img0[y1:y2, x1:x2]

        gray = cv2.cvtColor(lp, cv2.COLOR_BGR2GRAY)
        if debug:
            cv2.imwrite(f'preprocessed_license_plate_gray.jpg', gray)

        thresh, img0_bw = cv2.threshold(gray, 165, 255, cv2.THRESH_BINARY)
        if debug:
            cv2.imwrite(f'preprocessed_license_plate_img0_bw.jpg', img0_bw)

        noBoarder = self.removeBorder(img0_bw)
        if debug:
            cv2.imwrite(f'preprocessed_license_plate_noBoarder.jpg', noBoarder)

        #OCR
        reader = easyocr.Reader(['en'])
        result = reader.readtext(noBoarder)

        #Regex to ensure only valid symbols
        pattern = re.compile(r'[^a-zA-Z0-9]')

        filtered_text = None
        # Print the extracted text
        for detection in result:
            print(f"detection[1]: {detection[1]}")
            filtered_text = re.sub(pattern, '', detection[1])
            print("Extracted Text:", filtered_text)
        return result

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
        x1, y1, x2, y2, conf, cls_id = lp
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

    def runLPDetection(self, img0):
        model = YOLO(LPR_MODEL)
        results = model.predict(img0)
        foundLPs = results[0].boxes.data.tolist()
        ocr = ZapsOCR()

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

                #draw line and do analysis
                LP_Text = ocr.analyzeLP(img0, bestLP)
                self.drawLP_polylines(img0, bestLP)
                print(f"LP_Text: {LP_Text}")

        return img0

    def run_parking_detection(self, image_path: str, cam_num: str, building_name:str):
        self.json = self.load_camera_vertices(cam_num=cam_num, building_name=building_name)
        imgBGR = cv2.imread(image_path)
        if imgBGR is None:
            print(f"Could not open {image_path}")
            return

        results = self.model.track(imgBGR, persist = True, show = False)
        if results and results[0].boxes:
            car_occupancy = self.process_data(imgBGR)
            carLPs = self.runLPDetection(car_occupancy)
            cv2.imwrite(image_path, carLPs)
            print("Saved img!!")