import os
import pandas as pd
from ultralytics import YOLO

IMAGE_BASE = "data/raw/images"
OUTPUT_FILE = "data/yolo_detections.csv"

model = YOLO("yolov8n.pt")

results_list = []

for channel in os.listdir(IMAGE_BASE):
    channel_path = os.path.join(IMAGE_BASE, channel)
    if not os.path.isdir(channel_path):
        continue

    for img in os.listdir(channel_path):
        img_path = os.path.join(channel_path, img)
        message_id = img.replace(".jpg", "")

        results = model(img_path, verbose=False)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls]

                results_list.append({
                    "message_id": message_id,
                    "channel_name": channel,
                    "detected_object": label,
                    "confidence_score": conf
                })

df = pd.DataFrame(results_list)
df.to_csv(OUTPUT_FILE, index=False)

print("YOLO detection completed.")
