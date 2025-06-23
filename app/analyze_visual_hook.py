import json
from collections import Counter

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_hook_time_ranges(structured_transcript, fps=2):
    # Получаем все времена, где section == Hook
    return [round(entry["time"], 2) for entry in structured_transcript if entry["section"] == "Hook"]

def find_hook_frames(hook_times, fps=2):
    # Преобразуем времена в номера кадров
    return [f"frame_{int(t * fps):05}.jpg" for t in hook_times]

def collect_objects_per_frames(frame_list, yolo_objects):
    all_objs = []
    for fname in frame_list:
        objects = yolo_objects.get(fname, [])
        all_objs.extend([obj["label"] for obj in objects])
    return Counter(all_objs)

def main():
    transcript = load_json("data/structured_transcript.json")
    yolo_objects = load_json("data/objects_yolo.json")

    hook_times = get_hook_time_ranges(transcript)
    hook_frames = find_hook_frames(hook_times)

    obj_counts = collect_objects_per_frames(hook_frames, yolo_objects)

    print("🎯 Объекты в речевом Hook:")
    for label, count in obj_counts.most_common():
        print(f"- {label}: {count}")

    with open("data/hook_visual_objects.json", "w", encoding="utf-8") as f:
        json.dump(dict(obj_counts), f, ensure_ascii=False, indent=2)

    print("✅ Список объектов для Hook сохранён в data/hook_visual_objects.json")

if __name__ == "__main__":
    main()
