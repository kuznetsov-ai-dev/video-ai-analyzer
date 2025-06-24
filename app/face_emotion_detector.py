import os
from deepface import DeepFace
from PIL import Image
import cv2

def analyze_face_emotion(frame_path):
    try:
        result = DeepFace.analyze(
            img_path=frame_path,
            actions=["emotion"],
            enforce_detection=False,  # отключаем жёсткий режим
            detector_backend="opencv",  # используем OpenCV — стабильный
            prog_bar=False
        )
        return result[0]
    except Exception:
        return None

def run_analysis(frames_dir="data/frames", output_path="data/emotions.txt"):
    frames = sorted(os.listdir(frames_dir))
    frames = [f for f in frames if f.endswith(".jpg")]

    results = []
    for fname in frames:
        frame_path = os.path.join(frames_dir, fname)
        analysis = analyze_face_emotion(frame_path)
        if analysis:
            emotion = analysis["dominant_emotion"]
            confidence = analysis["emotion"][emotion]
            results.append(f"{fname}: {emotion} ({confidence:.1f}%)")
        else:
            results.append(f"{fname}: ❌ лицо не найдено")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"✅ Готово. Анализ завершён. Сохранено в {output_path}")

if __name__ == "__main__":
    run_analysis()
