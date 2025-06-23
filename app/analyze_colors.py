import os
import json
import cv2
import numpy as np
from collections import Counter

def extract_dominant_color(hsv_img):
    # Получаем основной оттенок (Hue)
    h = hsv_img[..., 0].flatten()
    counts = Counter(h)
    dominant = counts.most_common(1)[0][0]
    return int(dominant)

def compute_saturation(hsv_img):
    return float(hsv_img[..., 1].mean())

def compute_contrast(gray_img):
    return float(np.std(gray_img))  # стандартное отклонение яркости

def analyze_colors(frames_dir="data/frames", output_path="data/color_profile.json"):
    frames = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])
    results = []

    for fname in frames:
        path = os.path.join(frames_dir, fname)
        img = cv2.imread(path)

        if img is None:
            continue

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        dominant_hue = extract_dominant_color(hsv)
        saturation = compute_saturation(hsv)
        contrast = compute_contrast(gray)

        results.append({
            "frame": fname,
            "dominant_hue": dominant_hue,
            "saturation": round(saturation, 2),
            "contrast": round(contrast, 2)
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Цветовой профиль сохранён в {output_path}")

if __name__ == "__main__":
    analyze_colors()
