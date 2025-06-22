import os
import subprocess
import whisper
import sys

def extract_audio(input_video_path, output_audio_path):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio_path
    ]
    subprocess.run(command, check=True)
    print("✅ Аудио извлечено")

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    print("✅ Транскрипция завершена")
    return result

if __name__ == "__main__":
    input_video = sys.argv[1]
    output_audio = "data/audio.wav"

    extract_audio(input_video, output_audio)
    result = transcribe_audio(output_audio)

    with open("data/transcript.txt", "w", encoding="utf-8") as f:
        f.write(result["text"])
