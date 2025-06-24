import re

def split_sentences(input_path="data/transcript.txt", output_path="data/transcript.txt"):
    with open(input_path, "r", encoding="utf-8") as f:
        full_text = f.read().strip()

    # Разбиваем по знакам конца предложения + пробел
    sentences = re.split(r'(?<=[.!?])\s+', full_text)

    # Удаляем пустые
    sentences = [s.strip() for s in sentences if s.strip()]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sentences))

    print(f"✅ Разбито на {len(sentences)} предложений и записано в {output_path}")

if __name__ == "__main__":
    split_sentences()
