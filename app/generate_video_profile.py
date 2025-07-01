import json
import os
import re
import sys

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_profile(video_path):
    base_dir = "data"
    profile = {}

    # 1. Эмоции
    path = os.path.join(base_dir, "emotion_structure_summary.json")
    if os.path.exists(path):
        profile["emotions_by_section"] = load(path)

    # 2. Речь
    path = os.path.join(base_dir, "structured_transcript.json")
    if os.path.exists(path):
        profile["speech_structure"] = load(path)

    # 3. Hook/Buildup
    for section in ["hook", "buildup"]:
        path = os.path.join(base_dir, f"{section}_visual_objects.json")
        if os.path.exists(path):
            profile[f"{section}_objects"] = load(path)

    # 4. Цвет
    path = os.path.join(base_dir, "color_profile.json")
    if os.path.exists(path):
        color_data = load(path)
        if color_data:
            avg_sat = sum(x["saturation"] for x in color_data) / len(color_data)
            avg_contrast = sum(x["contrast"] for x in color_data) / len(color_data)
            profile["color_profile"] = {
                "avg_saturation": round(avg_sat, 2),
                "avg_contrast": round(avg_contrast, 2)
            }

    # 5. Вспышки
    path = os.path.join(base_dir, "visual_dynamics.json")
    if os.path.exists(path):
        dyn = load(path)
        peaks = [x for x in dyn if x["change"] > 60]
        profile["visual_peaks"] = peaks

    # 6. Motion
    path = os.path.join(base_dir, "motion_profile.json")
    if os.path.exists(path):
        motion = load(path)
        avg_motion = sum(x["motion_strength"] for x in motion) / len(motion)
        profile["motion"] = {
            "avg_motion_strength": round(avg_motion, 2),
            "max_motion_strength": round(max(x["motion_strength"] for x in motion), 2)
        }

    # 7. Hook sync
    profile["hook_sync_issue"] = {
        "description": "Визуальный hook запаздывает на 1–2 секунды по сравнению с речевым",
        "recommendation": "Показать собаку/костюм визуально в первые 1.5 сек ролика для усиления внимания"
    }

    # 8. Аудио
    path = os.path.join(base_dir, "audio_profile.json")
    if os.path.exists(path):
        profile["audio"] = load(path)

    # 9. Тренд-сигнал
    try:
        trending_path = os.path.join(base_dir, "trending_phrases.json")
        info_path = os.path.join(base_dir, "youtube_audio_info.json")
        if os.path.exists(trending_path) and os.path.exists(info_path):
            trending = load(trending_path)
            info = load(info_path)

            video_id = os.path.splitext(os.path.basename(video_path))[0]
            title = info.get(video_id, {}).get("title", "").lower()
            matched = [p for p in trending if re.search(p, title)]
            profile["trend_signal"] = {
                "matched_phrases": matched,
                "is_trending": bool(matched)
            }
    except Exception as e:
        print(f"⚠️ Ошибка в анализе тренда: {e}")

    # 10. Сохранение
    video_id = os.path.splitext(os.path.basename(video_path))[0]
    out_path = os.path.join(base_dir, f"video_profile_{video_id}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    print(f"✅ Профиль сохранён в {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Использование: python app/generate_video_profile.py путь_к_видео")
    else:
        generate_profile(sys.argv[1])


