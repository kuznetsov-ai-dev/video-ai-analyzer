import os
import cv2
import json
import numpy as np

def compute_brightness(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    return hsv[..., 2].mean()  # яркость = значение V из HSV

def compute_change(prev, curr):
    diff = cv2.absdiff(prev, curr)
    return np.mean(diff)

def analyze_frames(frames_dir="data/frames", output_path="data/visual_dynamics.json"):
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])
    dynamics = []

    prev_frame = None

    for i, fname in enumerate(frames):
        path = os.path.join(frames_dir, fname)
        curr = cv2.imread(path)

        if curr is None:
            continue

        brightness = compute_brightness(curr)

        if prev_frame is not None:
            if prev_frame.shape != curr.shape:
                curr = cv2.resize(curr, (prev_frame.shape[1], prev_frame.shape[0]))
            change = compute_change(prev_frame, curr)
        else:
            change = 0

        dynamics.append({
            "frame": fname,
            "brightness": round(float(brightness), 2),
            "change": round(float(change), 2)
        })

        prev_frame = curr

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dynamics, f, indent=2)

    print(f"✅ Анализ визуальной динамики завершён. Сохранено в {output_path}")

if __name__ == "__main__":
    analyze_frames()

