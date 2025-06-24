import os
import cv2
from deepface import DeepFace

def detect_faces_and_emotions(frames_dir="data/frames", output_path="data/emotions_opencv.txt"):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    frames = sorted(os.listdir(frames_dir))
    frames = [f for f in frames if f.endswith(".jpg")]

    results = []

    for fname in frames:
        frame_path = os.path.join(frames_dir, fname)
        image = cv2.imread(frame_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        if len(faces) == 0:
            results.append(f"{fname}: ❌ лицо не найдено")
            continue

        (x, y, w, h) = faces[0]
        face_img = image[y:y+h, x:x+w]

        # сохраняем временный файл
        temp_face_path = "temp_face.jpg"
        cv2.imwrite(temp_face_path, face_img)

        try:
            result = DeepFace.analyze(
                img_path=temp_face_path,
                actions=["emotion"],
                enforce_detection=False,
                detector_backend="opencv",
                prog_bar=False
            )
            emotion = result[0]["dominant_emotion"]
            confidence = result[0]["emotion"][emotion]
            results.append(f"{fname}: {emotion} ({confidence:.1f}%)")
        except Exception as e:
            results.append(f"{fname}: ❌ анализ не удался")
        finally:
            if os.path.exists(temp_face_path):
                os.remove(temp_face_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"✅ Готово. Эмоции найдены на {len([r for r in results if '❌' not in r])} кадрах")

if __name__ == "__main__":
    detect_faces_and_emotions()

