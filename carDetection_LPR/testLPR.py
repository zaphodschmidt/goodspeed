import cv2
from ultralytics import YOLO
import os
import numpy as np
import pytesseract
import easyocr

def noiseRemoval(image):
    import numpy as np
    kernel = np.ones((1,1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1,1),np.uint8)
    image = cv2.erode(image, kernel, iterations=1)

    # #Gets rid of noise
    # image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    # image = cv2.medianBlur(image,3)
    return image

def thinFont(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    #maks thinner
    kernel = np.ones((2,2), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

def thickFont(image):
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
def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)

def removeBorders(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntSorted = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    cnt = cntSorted[0]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return crop

def analyzeLP(img0, bestLP):
    x1, y1, x2, y2, conf, cls_id = bestLP
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    lp = img0[y1:y2, x1:x2]

    cv2.imwrite('preprocessed_license_plate2.jpg', lp)
    text = pytesseract.image_to_string(lp, config='--psm 8')  # PSM 8 is for single line of text
    print("lp:", text.strip())

    # rotated = deskew(lp)
    # cv2.imwrite('preprocessed_license_plate_rotated.jpg', rotated)
    # text = pytesseract.image_to_string(rotated, config='--psm 8')  # PSM 8 is for single line of text
    # print("rotated:", text.strip())

    #Gray
    gray = cv2.cvtColor(lp, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('preprocessed_license_plate_gray.jpg', gray)
    # text = pytesseract.image_to_string(gray, config='--psm 8')  # PSM 8 is for single line of text
    # print("gray:", text.strip())

    thresh, img0_bw = cv2.threshold(gray, 165, 255, cv2.THRESH_BINARY)
    cv2.imwrite(f'preprocessed_license_plate_img0_bw.jpg', img0_bw)
    text = pytesseract.image_to_string(img0_bw, config='--psm 8')  # PSM 8 is for single line of text
    print("img0_bw:", text.strip())

    noBoarder = removeBorders(img0_bw)
    cv2.imwrite(f'preprocessed_license_plate_noBoarder.jpg', noBoarder)
    text = pytesseract.image_to_string(noBoarder, config='--psm 8')  # PSM 8 is for single line of text
    print("noBoarder:", text.strip())

    noNoise = noiseRemoval(noBoarder)
    cv2.imwrite(f'preprocessed_license_plate_noNoise.jpg', noNoise)
    text = pytesseract.image_to_string(noNoise, config='--psm 8')  # PSM 8 is for single line of text
    print("noNoise:", text.strip())

    # thin = thinFont(noBoarder)
    # cv2.imwrite(f'preprocessed_license_plate_thin.jpg', thin)
    # text = pytesseract.image_to_string(thin, config='--psm 8')  # PSM 8 is for single line of text
    # print("thin:", text.strip())

    # #blurred
    # blurred = cv2.GaussianBlur(noBoarder, (5, 5), 0)
    # cv2.imwrite('preprocessed_license_plate_blurred.jpg', blurred)
    # text = pytesseract.image_to_string(blurred, config='--psm 8')  # PSM 8 is for single line of text
    # print("blurred:", text.strip())

  

    # thick_BW = thickFont(img0_bw)
    # cv2.imwrite(f'preprocessed_license_plate_thick_BW.jpg', thick_BW)
    # text = pytesseract.image_to_string(thick_BW, config='--psm 8')  # PSM 8 is for single line of text
    # print("thick_BW:", text.strip())

    # thin = thinFont(noNoise)
    # cv2.imwrite(f'preprocessed_license_plate_thin.jpg', thin)
    # text = pytesseract.image_to_string(thin, config='--psm 8')  # PSM 8 is for single line of text
    # print("thin:", text.strip())

    # thick = thickFont(noNoise)
    # cv2.imwrite(f'preprocessed_license_plate_thick.jpg', thick)
    # text = pytesseract.image_to_string(thick, config='--psm 8')  # PSM 8 is for single line of text
    # print("thick:", text.strip())

    # inverted = cv2.bitwise_not(lp)
    # cv2.imwrite('preprocessed_license_plate_Inverted.jpg', inverted)
    # text = pytesseract.image_to_string(inverted, config='--psm 8')  # PSM 8 is for single line of text
    # print("inverted:", text.strip())


    # #threshold
    # _, thresholded = cv2.threshold(lp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imwrite('preprocessed_license_plate_threshold.jpg', thresholded)
    # text = pytesseract.image_to_string(thresholded, config='--psm 8')  # PSM 8 is for single line of text
    # print("Extracted License Plate Text:", text.strip())


def easyORC_Trial(imgPath):
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Read text from the image
    result = reader.readtext(imgPath)

    # Print the extracted text
    for detection in result:
        print("Extracted Text:", detection[1])

if __name__ == "__main__":
    imgPath = "./TESTLP.png"
    # x1=1556
    # y1=524
    # x2=1609
    # y2=555
    x1=1
    y1=1
    x2=50
    y2=30
    conf = None
    cls_id = None
    bestLP = [x1, y1, x2, y2, conf, cls_id]
    img0 = cv2.imread("./TESTLP.png")
    analyzeLP(img0, bestLP)
    easyORC_Trial('preprocessed_license_plate_noBoarder.jpg')
