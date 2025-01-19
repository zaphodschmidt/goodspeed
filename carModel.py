from ultralytics import YOLO, checks, hub
checks()

hub.login('2a1a443b20b14cf834a90455212c8e2447527a7c22')

model = YOLO('https://hub.ultralytics.com/models/VeIcAf98OeRUZ4totalp')
results = model.train()