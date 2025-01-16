from ultralytics import YOLO, checks, hub

checks()
hub.login('2a1a443b20b14cf834a90455212c8e2447527a7c22')
model = YOLO('https://hub.ultralytics.com/models/so9Q3LUuAH4M7ycWY9mp')
results = model.train()