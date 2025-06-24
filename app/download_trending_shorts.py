# app/download_trending_shorts.py

import scrapetube
import os
import yt_dlp

# 📁 Папка для сохранения видео
SAVE_DIR = "data/top_shorts"
os.makedirs(SAVE_DIR, exist_ok=True)

# 🔍 Поиск видео по ключевому слову "dance tutorial"
print("🔍 Поиск YouTube Shorts по запросу 'dance tutorial'...")
videos = scrapetube.get_search("dance tutorial", limit=10)

# 📥 Скачиваем ролики через yt-dlp
for i, video in enumerate(videos, 1):
    video_id = video['videoId']
    url = f"https://www.youtube.com/shorts/{video_id}"
    print(f"\n▶️ [{i}/10] Скачиваем: {url}")

    ydl_opts = {
        'outtmpl': f'{SAVE_DIR}/%(id)s.%(ext)s',
        'format': 'mp4[height<=720]',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"❌ Ошибка при скачивании {url}: {e}")
