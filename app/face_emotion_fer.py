import os
import cv2
from fer import FER

def detect_fer_emotions(frames_dir="data/frames", output_path="data/emotions_fer.txt"):
    detector = FER(mtcnn=True)
    frames = sorted(os.listdir(frames_dir))
    frames = [f for f in frames if f.endswith(".jpg")]

    results = []
    count_detected = 0

    for fname in frames:
        path = os.path.join(frames_dir, fname)
        img = cv2.imread(path)

        result = detector.top_emotion(img)

        if result is None or result[0] is None:
            results.append(f"{fname}: ❌ эмоция не определена")
        else:
            emotion, score = result
            results.append(f"{fname}: {emotion} ({score:.1%})")
            count_detected += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"✅ Готово. Эмоции найдены на {count_detected} кадрах из {len(frames)}")

if __name__ == "__main__":
    detect_fer_emotions()

