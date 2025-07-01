# app/youtube_extract_audio_info.py

import os
import yt_dlp
import json

VIDEOS_DIR = "data/top_shorts"
OUTPUT_PATH = "data/youtube_audio_info.json"

video_files = [f for f in os.listdir(VIDEOS_DIR) if f.endswith(".mp4")]
results = {}

for filename in video_files:
    video_id = os.path.splitext(filename)[0]
    url = f"https://www.youtube.com/shorts/{video_id}"

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            results[video_id] = {
                "title": info.get("title"),
                "track": info.get("track"),
                "artist": info.get("artist"),
                "uploader": info.get("uploader"),
                "url": url
            }
            print(f"✅ {video_id}: {info.get('track')} — {info.get('artist')}")
    except Exception as e:
        results[video_id] = {"error": str(e)}
        print(f"❌ {video_id}: ошибка — {e}")

# Сохраняем результат
os.makedirs("data", exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n📁 Результаты сохранены в {OUTPUT_PATH}")
