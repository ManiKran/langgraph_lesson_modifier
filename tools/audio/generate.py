# tools/audio/generate.py

import os
import uuid
from typing import List, Tuple
from openai import OpenAI

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Ensure output directory exists
OUTPUT_DIR = "data/outputs/audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def split_text_for_audio(text: str, num_chunks: int = 5) -> List[str]:
    """
    Splits the input text into `num_chunks` roughly equal-length chunks.
    """
    if not text:
        return []

    words = text.split()
    total_words = len(words)
    chunk_size = max(1, total_words // num_chunks)

    chunks = []
    for i in range(0, total_words, chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        if len(chunks) == num_chunks:
            break

    return chunks

def generate_audio_for_text_chunks(chunks: List[str]) -> List[Tuple[str, str]]:
    """
    Converts each text chunk into an audio file.
    Returns list of (audio_url, audio_text).
    """
    audio_results = []

    for idx, chunk in enumerate(chunks):
        if not chunk.strip():
            continue  # Skip empty parts

        try:
            filename = f"audio_{uuid.uuid4().hex}.mp3"
            audio_path = os.path.join(OUTPUT_DIR, filename)

            response = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="nova",  # or "shimmer", "onyx", etc.
                input=chunk
            )
            response.stream_to_file(audio_path)

            audio_url = f"https://langgraph-lesson-modifier.onrender.com/audio/{filename}"
            audio_results.append((audio_url, chunk.strip()))

            print(f"[AudioAgent] Generated audio for chunk {idx}: {audio_url}")
        except Exception as e:
            print(f"[AudioAgent] Failed to generate audio for chunk {idx}: {e}")
            continue

    return audio_results