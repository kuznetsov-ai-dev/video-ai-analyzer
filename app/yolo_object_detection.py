import os
import json
from ultralytics import YOLO
from PIL import Image

def detect_objects(frames_dir="data/frames", output_json="data/objects_yolo.json"):
    model = YOLO("yolov8n.pt")  # Можно заменить на yolov8s.pt для точности

    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])
    results = {}

    for fname in frames:
        path = os.path.join(frames_dir, fname)
        img = Image.open(path)

        detections = model(img)[0]  # получаем первый результат

        frame_objects = []
        for box in detections.boxes:
            cls_id = int(box.cls[0])
            name = model.names[cls_id]
            conf = float(box.conf[0])
            frame_objects.append({
                "label": name,
                "confidence": round(conf, 3)
            })

        results[fname] = frame_objects

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✅ Детекция завершена. Результат: {output_json}")

if __name__ == "__main__":
    detect_objects()
