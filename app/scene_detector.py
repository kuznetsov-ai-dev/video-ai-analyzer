import os
import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np

def read_image_gray(path):
    img = cv2.imread(path)
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def detect_scenes(frames_dir, threshold=0.90, min_gap=15):
    frames = sorted(os.listdir(frames_dir))
    frames = [f for f in frames if f.endswith(".jpg")]

    prev_frame = None
    scene_changes = []

    for i, fname in enumerate(frames):
        path = os.path.join(frames_dir, fname)
        gray = read_image_gray(path)

        if prev_frame is None:
            prev_frame = gray
            scene_changes.append((i, fname))  # первая сцена всегда
            continue

        score = ssim(prev_frame, gray)

        # Добавляем сцену только если достаточно отличий и прошло минимум min_gap кадров
        if score < threshold and (i - scene_changes[-1][0]) > min_gap:
            scene_changes.append((i, fname))

        prev_frame = gray

    return scene_changes

if __name__ == "__main__":
    scenes = detect_scenes("data/frames", threshold=0.88, min_gap=5)
    print(f"✅ Обнаружено {len(scenes)} сцен:")
    for i, (idx, fname) in enumerate(scenes):
        print(f"{i+1:02d}: кадр {idx} — {fname}")