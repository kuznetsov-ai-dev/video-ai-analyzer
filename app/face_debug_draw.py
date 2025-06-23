import cv2
import os

def draw_faces_on_frames(frames_dir="data/frames", output_dir="data/frames_faces"):
    os.makedirs(output_dir, exist_ok=True)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    frames = sorted(os.listdir(frames_dir))
    frames = [f for f in frames if f.endswith(".jpg")]

    count = 0
    for fname in frames:
        path = os.path.join(frames_dir, fname)
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if len(faces) > 0:
            out_path = os.path.join(output_dir, fname)
            cv2.imwrite(out_path, image)
            count += 1

    print(f"✅ Нарисовано рамок на {count} кадрах. Сохранили в {output_dir}")

if __name__ == "__main__":
    draw_faces_on_frames()
