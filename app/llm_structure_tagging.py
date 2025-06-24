import json
import requests

def load_transcript(path="data/transcript.txt", fps=2):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    transcript = []
    for i, line in enumerate(lines):
        time_sec = i / fps
        transcript.append({
            "time": round(time_sec, 2),
            "text": line.strip(),
        })

    return transcript

def ask_llm_to_tag(transcript_chunk):
    prompt = f"""
Разметь следующие строки речи по структуре видео: Hook, Buildup, Climax, CTA, Other.

Ответ в формате JSON: список объектов вида
[{{"text": "...", "section": "Hook"}}, ...]

Вот строки:
{[x['text'] for x in transcript_chunk]}
"""

    res = requests.post("http://localhost:1234/v1/completions", json={
        "prompt": prompt,
        "max_tokens": 1000,
        "temperature": 0.3,
        "stop": None,
    })

    raw = res.json()
    text = raw['choices'][0]['text']

    try:
        parsed = json.loads(text)
        return parsed
    except Exception as e:
        print("⚠️ Ошибка разбора LLM-ответа:", e)
        print("Ответ был:", text)
        return []

def tag_transcript(transcript, chunk_size=10):
    result = []
    for i in range(0, len(transcript), chunk_size):
        chunk = transcript[i:i+chunk_size]
        llm_result = ask_llm_to_tag(chunk)
        for j, item in enumerate(llm_result):
            if j < len(chunk):
                entry = {
                    "time": chunk[j]["time"],
                    "text": chunk[j]["text"],
                    "section": item.get("section", "Other")
                }
                result.append(entry)
    return result

def save_tagged(data, path="data/structured_transcript.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Размеченный транскрипт сохранён в {path}")

if __name__ == "__main__":
    transcript = load_transcript()
    tagged = tag_transcript(transcript)
    save_tagged(tagged)
