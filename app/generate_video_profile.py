import json
import os

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_profile():
    base_dir = "data"
    profile = {}

    # 1. Эмоции по структурам
    path = os.path.join(base_dir, "emotion_structure_summary.json")
    if os.path.exists(path):
        profile["emotions_by_section"] = load(path)

    # 2. Структура речи
    path = os.path.join(base_dir, "structured_transcript.json")
    if os.path.exists(path):
        profile["speech_structure"] = load(path)

    # 3. Объекты по Hook и Buildup
    for section in ["hook", "buildup"]:
        path = os.path.join(base_dir, f"{section}_visual_objects.json")
        if os.path.exists(path):
            profile[f"{section}_objects"] = load(path)

    # 4. Цветовой профиль (усреднение)
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

    # 5. Вспышки (визуальные пики)
    path = os.path.join(base_dir, "visual_dynamics.json")
    if os.path.exists(path):
        dyn = load(path)
        peaks = [x for x in dyn if x["change"] > 60]
        profile["visual_peaks"] = peaks

    # 6. Motion (движение)
    path = os.path.join(base_dir, "motion_profile.json")
    if os.path.exists(path):
        motion = load(path)
        avg_motion = sum(x["motion_strength"] for x in motion) / len(motion)
        profile["motion"] = {
            "avg_motion_strength": round(avg_motion, 2),
            "max_motion_strength": round(max(x["motion_strength"] for x in motion), 2)
        }

    # 7. Hook sync issue (обнаружено нами вручную)
    profile["hook_sync_issue"] = {
        "description": "Визуальный hook запаздывает на 1–2 секунды по сравнению с речевым",
        "recommendation": "Показать собаку/костюм визуально в первые 1.5 сек ролика для усиления внимания"
    }

    # Сохранить
    out_path = os.path.join(base_dir, "video_profile.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)

    print(f"✅ Финальный профиль ролика сохранён в {out_path}")

if __name__ == "__main__":
    generate_profile()

