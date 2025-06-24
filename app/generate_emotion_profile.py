import json
import os

def parse_emotions_txt(emotions_path="data/emotions_fer.txt", fps=2):
    results = []

    with open(emotions_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or not line.startswith("frame_"):
            continue

        try:
            fname, rest = line.split(":", 1)
            frame_num = int(fname.replace("frame_", "").replace(".jpg", ""))
            time_sec = frame_num / fps

            if "❌" in rest or "эмоция не определена" in rest:
                emotion = "unknown"
                score = 0.0
            else:
                emotion_part, score_part = rest.strip().split(" (")
                emotion = emotion_part.strip()
                score = float(score_part.strip(")%")) / 100

            results.append({
                "frame": fname,
                "time": round(time_sec, 2),
                "emotion": emotion,
                "score": round(score, 3)
            })

        except Exception as e:
            print(f"⚠️ Проблема с парсингом строки: {line} → {e}")

    return results

def save_json(data, output_path="data/emotions_profile.json"):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Эмоциональный профиль сохранён: {output_path}")

if __name__ == "__main__":
    emotions = parse_emotions_txt()
    save_json(emotions)
