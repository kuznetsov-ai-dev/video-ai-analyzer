import cv2
import os
import sys

def extract_frames(video_path, output_folder="data/frames", interval_sec=0.5):
    os.makedirs(output_folder, exist_ok=True)

    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)

    count = 0
    saved = 0
    success, image = vidcap.read()

    while success:
        if count % frame_interval == 0:
            filename = f"{output_folder}/frame_{saved:05d}.jpg"
            cv2.imwrite(filename, image)
            saved += 1
        success, image = vidcap.read()
        count += 1

    vidcap.release()
    print(f"✅ Извлечено {saved} кадров в папку: {output_folder}")

if __name__ == "__main__":
    video_path = sys.argv[1]
    extract_frames(video_path)
