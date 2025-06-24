# app/batch_analyze_trending.py
import os
import subprocess
import shutil

VIDEOS_DIR = "data/top_shorts"
RESULTS_DIR = "data/top_shorts_profiles"
os.makedirs(RESULTS_DIR, exist_ok=True)

video_files = [f for f in os.listdir(VIDEOS_DIR) if f.endswith(".mp4")]

for idx, video_file in enumerate(video_files, 1):
    video_path = os.path.join(VIDEOS_DIR, video_file)
    video_id = os.path.splitext(video_file)[0]

    print(f"\n🌀 [{idx}/{len(video_files)}] Анализируем: {video_file}")

    try:
        # Запуск полного пайплайна
        subprocess.run(["python", "app/pipeline_full.py", video_path], check=True)

        # Копирование результата
        src = "data/video_profile.json"
        dst = os.path.join(RESULTS_DIR, f"video_profile_{video_id}.json")
        shutil.copyfile(src, dst)

        print(f"✅ Профиль сохранён: {dst}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при обработке {video_file}: {e}")
        continue
