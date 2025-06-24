import os
import cv2
import json
import numpy as np

def compute_motion(prev_gray, curr_gray):
    # Подгоняем размер, если не совпадает
    if prev_gray.shape != curr_gray.shape:
        curr_gray = cv2.resize(curr_gray, (prev_gray.shape[1], prev_gray.shape[0]))
    
    flow = cv2.calcOpticalFlowFarneback(
        prev_gray, curr_gray, None,
        0.5, 3, 15, 3, 5, 1.2, 0
    )
    magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    return float(np.mean(magnitude))  # средняя "сила" движения

def analyze_motion(frames_dir="data/frames", output_path="data/motion_profile.json"):
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])
    motion_data = []

    prev_gray = None

    for fname in frames:
        path = os.path.join(frames_dir, fname)
        img = cv2.imread(path)

        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if prev_gray is None:
            motion = 0.0
        else:
            motion = compute_motion(prev_gray, gray)

        motion_data.append({
            "frame": fname,
            "motion_strength": round(motion, 4)
        })

        prev_gray = gray

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(motion_data, f, indent=2)

    print(f"✅ Анализ движения завершён. Сохранено в {output_path}")

if __name__ == "__main__":
    analyze_motion()

