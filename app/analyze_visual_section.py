import json
from collections import Counter

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_section_time_ranges(structured_transcript, section="Buildup", fps=2):
    return [round(entry["time"], 2) for entry in structured_transcript if entry["section"] == section]

def find_section_frames(times, fps=2):
    return [f"frame_{int(t * fps):05}.jpg" for t in times]

def collect_objects_per_frames(frame_list, yolo_objects):
    all_objs = []
    for fname in frame_list:
        objects = yolo_objects.get(fname, [])
        all_objs.extend([obj["label"] for obj in objects])
    return Counter(all_objs)

def main(section="Buildup"):
    transcript = load_json("data/structured_transcript.json")
    yolo_objects = load_json("data/objects_yolo.json")

    section_times = get_section_time_ranges(transcript, section)
    section_frames = find_section_frames(section_times)

    obj_counts = collect_objects_per_frames(section_frames, yolo_objects)

    print(f"🎯 Объекты в секции {section}:")
    for label, count in obj_counts.most_common():
        print(f"- {label}: {count}")

    with open(f"data/{section.lower()}_visual_objects.json", "w", encoding="utf-8") as f:
        json.dump(dict(obj_counts), f, ensure_ascii=False, indent=2)

    print(f"✅ Объекты для {section} сохранены в data/{section.lower()}_visual_objects.json")

if __name__ == "__main__":
    main("Buildup")  # ← можно заменить на любую секцию
