import librosa
import librosa.display
import numpy as np
import json
import matplotlib.pyplot as plt
import os

def analyze_audio(audio_path="data/audio.wav", output_json="data/audio_profile.json"):
    y, sr = librosa.load(audio_path, sr=None)
    
    # Громкость (энергия)
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.times_like(rms, sr=sr)

    # Найти пики (всплески звука)
    peaks = librosa.util.peak_pick(rms, pre_max=10, post_max=10, pre_avg=20, post_avg=20, delta=0.02, wait=5)

    # BPM (темп)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Средняя громкость
    avg_rms = float(np.mean(rms))
    max_rms = float(np.max(rms))

    result = {
        "duration_sec": round(len(y) / sr, 2),
        "avg_rms": round(avg_rms, 4),
        "max_rms": round(max_rms, 4),
        "peak_count": len(peaks),
        "peak_times": [round(times[p], 2) for p in peaks],
        "estimated_bpm": round(float(tempo), 2)
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Аудио-профиль сохранён в {output_json}")

if __name__ == "__main__":
    analyze_audio()
