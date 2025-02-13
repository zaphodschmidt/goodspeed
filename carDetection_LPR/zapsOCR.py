import cv2
import easyocr
import re

class ZapsOCR():
    def __init__(self) -> None:
        pass

    def noiseRemoval(self, image):
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