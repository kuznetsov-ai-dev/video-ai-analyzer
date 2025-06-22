import streamlit as st
import os
import subprocess
from llm_analysis import load_transcript, build_prompt, ask_llm, save_report

st.set_page_config(page_title="AI-анализ коротких видео", layout="centered")
st.title("🎬 AI-анализ коротких видео")
st.markdown("## 📥 Загрузка видео")

video_file = st.file_uploader("Загрузите видеофайл", type=["mp4", "mov", "webm"])
video_url = st.text_input("...или вставьте ссылку на видео (опционально)")

if st.button("▶️ Запустить анализ"):
    with st.spinner("Анализируем видео..."):
        os.makedirs("data", exist_ok=True)
        video_path = "data/input_video.mp4"

        if video_file:
            with open(video_path, "wb") as f:
                f.write(video_file.read())
        elif video_url:
            subprocess.run(["yt-dlp", video_url, "-o", video_path])
        else:
            st.warning("Загрузите файл или вставьте ссылку.")
            st.stop()

        subprocess.run(["python", "app/pipeline.py", video_path], check=True)

        transcript_path = "data/transcript.txt"
        if os.path.exists(transcript_path):
            transcript = load_transcript(transcript_path)
            prompt = build_prompt(transcript)
            response = ask_llm(prompt)
            save_report(response)

        report_path = "data/report.txt"
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                report = f.read()
            st.markdown("## 📄 Результат анализа")
            st.markdown(report, unsafe_allow_html=True)
        else:
            st.error("report.txt не найден")
