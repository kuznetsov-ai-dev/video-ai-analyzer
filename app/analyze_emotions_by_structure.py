import json
from collections import defaultdict, Counter

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def match_emotion_to_section(emotions, transcript, max_gap=0.5):
    # строим тайм-интервалы по секциям
    section_map = {}
    for item in transcript:
        t = item["time"]
        section_map[round(t, 2)] = item["section"]

    matched = defaultdict(list)
    for emo in emotions:
        time = round(emo["time"], 2)
        # ищем ближайшую секцию
        section = section_map.get(time)
        if not section:
            # ищем ближайшую в пределах max_gap
            nearby = [s for t2, s in section_map.items() if abs(t2 - time) <= max_gap]
            section = nearby[0] if nearby else "Other"

        if emo["emotion"] != "unknown":
            matched[section].append(emo)

    return matched

def summarize(matched):
    summary = {}
    for section, emos in matched.items():
        scores = [e["score"] for e in emos]
        emotions = [e["emotion"] for e in emos]
        if not scores:
            continue
        avg = sum(scores) / len(scores)
        dominant = Counter(emotions).most_common(1)[0][0]
        summary[section] = {
            "dominant_emotion": dominant,
            "avg_score": round(avg, 3),
            "count": len(emos)
        }
    return summary

def main():
    emotions = load_json("data/emotions_profile.json")
    transcript = load_json("data/structured_transcript.json")
    matched = match_emotion_to_section(emotions, transcript)
    summary = summarize(matched)

    with open("data/emotion_structure_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("✅ Эмоциональный анализ по структурам сохранён в data/emotion_structure_summary.json")

if __name__ == "__main__":
    main()
