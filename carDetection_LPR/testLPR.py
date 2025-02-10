import cv2
from ultralytics import YOLO
import os
# import ET

def checkFrame():
    model = YOLO('best_model_NPT.pt')
    img = cv2.imread("car.jpeg")

    # Read a frame from the camera
    results = model.track(img,persist=True)
    for result in results[0].boxes.data.tolist():
        x1, y1, x2, y2, id, score,label = result

        #check if threshold met and object is a car
        # if score > 0.5 and label==2:
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
        text_x = int(x1)
        text_y = int(y1) - 10
        cv2.putText(img, str(id), (text_x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cropped_img = img[int(y1):int(y2), int(x1):int(x2)]
        cv2.imwrite(f"savedIMG_{id}.jpg.jpg",cropped_img)

    # cv2.imshow("Detected Cars", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    checkFrame()
