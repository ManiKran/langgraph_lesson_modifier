# tools/output/generate.py

import os
import uuid

OUTPUT_DIR = "data/outputs/final"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_final_output(lesson_text: str, image_paths: list, audio_paths: list) -> str:
    """
    Generates a final .txt file with embedded placeholders for images and audio.
    Replaces [IMAGE:filename] and [AUDIO:filename] with human-readable tags.
    """
    filename = f"final_lesson_{uuid.uuid4().hex}.txt"
    output_path = os.path.join(OUTPUT_DIR, filename)

    enriched_text = lesson_text

    # Replace [IMAGE:xxx] with actual image file info
    for path in image_paths:
        fname = os.path.basename(path)
        enriched_text = enriched_text.replace(f"[IMAGE:{fname}]", f"\n🔍 [Insert Image: {fname}]\n")

    # Replace [AUDIO:xxx] with actual audio file info
    for path in audio_paths:
        fname = os.path.basename(path)
        enriched_text = enriched_text.replace(f"[AUDIO:{fname}]", f"\n🔊 [Insert Audio: {fname}]\n")

    with open(output_path, "w") as f:
        f.write(enriched_text)

    return output_path