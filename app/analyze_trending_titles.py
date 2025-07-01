# app/analyze_trending_titles.py

import json
import re
from collections import Counter, defaultdict

INPUT_PATH = "data/youtube_audio_info.json"
TREND_THRESHOLD = 2  # минимум сколько раз должно встретиться

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Словарь: video_id -> title
titles = {vid: meta["title"] for vid, meta in data.items() if "title" in meta and meta["title"]}

# Нормализация: токенизация и удаление стоп-слов
stopwords = {"the", "to", "and", "a", "of", "in", "for", "it", "with", "on", "at", "by", "is", "i", "you", "this", "that"}

# Словарь: ключевая фраза -> список video_id
trends = defaultdict(list)

for vid, title in titles.items():
    title = title.lower()
    tokens = re.findall(r'\b\w+\b', title)
    filtered = [t for t in tokens if t not in stopwords]
    
    # создаём биграммы (2-словные фразы)
    bigrams = zip(filtered, filtered[1:])
    phrases = [" ".join(pair) for pair in bigrams]
    
    for phrase in phrases:
        trends[phrase].append(vid)

# Подсчёт
print("🎵 Потенциально трендовые ключевые фразы:\n")
for phrase, vids in sorted(trends.items(), key=lambda x: -len(x[1])):
    if len(vids) >= TREND_THRESHOLD:
        print(f"🔹 '{phrase}' — использовано в {len(vids)} видео:")
        for vid in vids:
            print(f"    • {vid} → {titles[vid]}")
        print()
