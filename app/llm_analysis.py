# app/llm_analysis.py

import requests
import json

API_URL = "http://localhost:1234/v1/chat/completions"  # LM Studio API

def load_transcript(path="data/transcript.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def build_prompt(transcript):
    return f"""
Ниже транскрипт короткого видео (Reels/TikTok):

{transcript}

Разбери структуру ролика и верни отчёт на русском языке, строго по этому формату:

🎯 **Крючок** — что цепляет в начале?

🔄 **Развитие** — где развитие, как растёт интрига?

🔥 **Кульминация** — есть ли кульминация?

🎬 **Призыв к действию** — есть ли призыв к действию?

🎭 **Эмоции и триггеры** — что вызывает интерес? юмор? повторения?

⏱️ **Ритм и паузы** — как построено напряжение?

✅ **Анализ и советы** — что хорошо, что можно улучшить?

Ответ только по формату. Язык — русский. Будь кратким и точным.
"""

def ask_llm(prompt):
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "mistral",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2048,
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

def save_report(content, path="data/report.txt"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    transcript = load_transcript()
    prompt = build_prompt(transcript)
    result = ask_llm(prompt)
    save_report(result)
    print("✅ Анализ завершён. Отчёт сохранён в data/report.txt")
