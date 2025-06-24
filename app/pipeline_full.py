# app/pipeline_full.py

import os
import subprocess
import sys

def run(cmd, desc):
    print(f"\n▶️ {desc}...")
    subprocess.run(cmd, check=True)
    print(f"✅ {desc} — выполнено.")

def main(video_path):
    os.makedirs("data", exist_ok=True)

    # 1. Аудио и транскрипт
    run(["python", "app/pipeline.py", video_path], "Извлечение аудио + транскрипция Whisper")

    # 2. Разбивка транскрипта на предложения
    run(["python", "app/split_transcript_sentences.py"], "Разбивка транскрипта на предложения")

    # 3. Кадры
    run(["python", "app/video_to_frames.py", video_path], "Извлечение кадров из видео")

    # 4. Эмоции (FER)
    run(["python", "app/face_emotion_fer.py"], "Распознавание эмоций (FER)")

    # 5. JSON эмоций
    run(["python", "app/generate_emotion_profile.py"], "Формирование JSON эмоций")

    # 6. LLM-теггинг структуры
    run(["python", "app/llm_structure_tagging.py"], "LLM-разметка структуры")

    # 7. Сопоставление эмоций с речью
    run(["python", "app/analyze_emotions_by_structure.py"], "Сопоставление эмоций с секциями")

    # 8. YOLO
    run(["python", "app/yolo_object_detection.py"], "Обнаружение объектов (YOLOv8)")

    # 9. Hook + buildup визуальные
    run(["python", "app/analyze_visual_hook.py"], "Hook-объекты (визуально)")
    run(["python", "app/analyze_visual_section.py"], "Buildup-объекты (визуально)")

    # 10. Цвет, динамика, движение
    run(["python", "app/analyze_colors.py"], "Цветовой анализ")
    run(["python", "app/analyze_visual_dynamics.py"], "Анализ яркости и вспышек")
    run(["python", "app/analyze_motion.py"], "Анализ движения")

    # 11. Финальный JSON
    run(["python", "app/generate_video_profile.py"], "Генерация финального профиля")

    print("\n🏁 Все шаги завершены. Финальный JSON: data/video_profile.json")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Использование: python app/pipeline_full.py путь_к_видео")
        sys.exit(1)
    main(sys.argv[1])
