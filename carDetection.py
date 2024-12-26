from ultralytics import YOLO

model = YOLO('yolov8n.pt')
results = model('./testpic.jpeg')

CAR_CLASS_ID = 2

for result in results:
    for box in result.boxes:
        cls_id = int(box.cls)
        conf = float(box.conf)
        x_min, y_min, x_max, y_max = box.xyxy[0]

        if cls_id == CAR_CLASS_ID:
            print(f"Car detected with confidence {conf:.2f}")
            print(f"Bounding box: x_min={x_min:.2f}, y_min={y_min:.2f}, x_max={x_max:.2f}, y_max={y_max:.2f}\n")
for r in results:
    r.show()