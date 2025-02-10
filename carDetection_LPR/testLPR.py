import cv2
from ultralytics import YOLO
import os
import numpy as np

def checkFrame():
    model = YOLO('best_model_NPT.pt')
    img = cv2.imread("camera_snapshot_20250209170009_vertex1_cam6.jpeg")
    results = model.track(img,persist=True)

    for result in results[0].boxes.data.tolist():
        x1, y1, x2, y2, id, score,label = result

        # if score > 0.5 and label==2:
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
        pts = np.array([
            [int(x1), int(y1)],
            [int(x2), int(y1)],
            [int(x2), int(y2)],
            [int(x1), int(y2)]
        ], np.int32)
        
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

    cv2.imwrite(f"savedIMG_{id}.jpg.jpg",img)

if __name__ == "__main__":
    checkFrame()
