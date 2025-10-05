import os
import uuid
import json
import re

OUTPUT_DIR = "data/outputs/final"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_AUDIO_URL = "https://langgraph-lesson-modifier.onrender.com/audio/"
BASE_IMAGE_URL = "https://langgraph-lesson-modifier.onrender.com/images/"

def generate_final_output(lesson_text: str, image_paths: list, audio_paths: list) -> dict:
    """
    Generates:
    1) A .txt file with embedded placeholders (like before)
    2) A .json file with a structured array of content blocks for frontend rendering
    """
    file_id = uuid.uuid4().hex
    txt_filename = f"final_lesson_{file_id}.txt"
    json_filename = f"final_lesson_{file_id}.json"

    txt_path = os.path.join(OUTPUT_DIR, txt_filename)
    json_path = os.path.join(OUTPUT_DIR, json_filename)

    # --- 1) Enrich text file (what you had before) ---
    enriched_text = lesson_text
    for path in image_paths:
        fname = os.path.basename(path)
        enriched_text = enriched_text.replace(f"[IMAGE:{fname}]", f"\n🔍 [Insert Image: {fname}]\n")

    for path in audio_paths:
        fname = os.path.basename(path)
        enriched_text = enriched_text.replace(f"[AUDIO:{fname}]", f"\n🔊 [Insert Audio: {fname}]\n")

    with open(txt_path, "w") as f:
        f.write(enriched_text)

    # --- 2) Build JSON blocks ---
    blocks = []
    lines = enriched_text.splitlines()
    for line in lines:
        # Audio placeholder
        audio_match = re.search(r"\[Insert Audio:\s*(.+?)\]", line)
        if audio_match:
            fname = audio_match.group(1).strip()
            # Add full URL
            blocks.append({
                "type": "audio",
                "src": f"{BASE_AUDIO_URL}{fname}"
            })
            continue

        # Image placeholder
        image_match = re.search(r"\[Insert Image:\s*(.+?)\]", line)
        if image_match:
            fname = image_match.group(1).strip()
            blocks.append({
                "type": "image",
                "src": f"{BASE_IMAGE_URL}{fname}"
            })
            continue

        # Otherwise, if text line has content
        text_content = line.strip()
        if text_content:
            blocks.append({
                "type": "text",
                "content": text_content
            })

    # Save JSON file
    with open(json_path, "w") as jf:
        json.dump(blocks, jf, ensure_ascii=False, indent=2)

    # Return both paths so the state can hold them
    return {
        "txt_path": txt_path,
        "json_path": json_path
    }