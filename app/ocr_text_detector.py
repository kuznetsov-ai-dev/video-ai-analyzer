import os
import cv2
import pytesseract
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_frame(frame_path):
    image = cv2.imread(frame_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # повышаем контрастность и бинаризуем
    processed = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    # можно добавить размытие или морфологию при необходимости
    pil_img = Image.fromarray(processed)
    text = pytesseract.image_to_string(pil_img, lang="eng+rus")
    return text.strip()

def run_ocr_on_scenes(frames_dir="data/frames", output_path="data/ocr_scenes.txt"):
    frames = sorted(os.listdir(frames_dir))
    frames = [f for f in frames if f.startswith("frame_") and f.endswith(".jpg")]

    result = []
    for fname in frames:
        frame_path = os.path.join(frames_dir, fname)
        text = extract_text_from_frame(frame_path)
        if text:
            result.append(f"{fname}:\n{text}\n{'-'*30}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(result))

    print(f"✅ Готово: найден текст на {len(result)} кадрах. Сохранено в {output_path}")

if __name__ == "__main__":
    run_ocr_on_scenes()


