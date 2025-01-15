from ultralytics import YOLO
import os
import imghdr
from PIL import Image

# test_file = "./backend/media/uploads/camera_snapshot_20250114192003_cam5.jpg"
# img = Image.open(test_file)
# img.show()

def is_jpeg(file_path):
    try:
        with Image.open(file_path) as img:
            return img.format == 'JPEG'
    except (IOError, OSError):
        return False

PATH = './backend/media/uploads'
def getDirs(path: str):
    files = []
    for fileName in os.scandir(path):
        if fileName.is_file() and is_jpeg(fileName):
            files.append(PATH+"/"+fileName.name)
    return files

fileList = getDirs(PATH)
print(fileList)
model = YOLO('yolov8n.pt')
results = model(source = fileList, show = True, conf = 0.4, save = True)

# CAR_CLASS_ID = 2

# for result in results:
#     for box in result.boxes:
#         cls_id = int(box.cls)
#         conf = float(box.conf)
#         x_min, y_min, x_max, y_max = box.xyxy[0]

#         if cls_id == CAR_CLASS_ID:
#             print(f"Car detected with confidence {conf:.2f}")
#             print(f"Bounding box: x_min={x_min:.2f}, y_min={y_min:.2f}, x_max={x_max:.2f}, y_max={y_max:.2f}\n")
# for r in results:
#     r.show()