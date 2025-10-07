import os
import uuid
import json
import re
import urllib.parse

FINAL_TXT_DIR = "data/outputs/final"
FINAL_JSON_DIR = "data/outputs/json"
FINAL_MD_DIR = "data/outputs/markdown"

os.makedirs(FINAL_TXT_DIR, exist_ok=True)
os.makedirs(FINAL_JSON_DIR, exist_ok=True)
os.makedirs(FINAL_MD_DIR, exist_ok=True)

BASE_AUDIO_URL = "https://langgraph-lesson-modifier.onrender.com/audio/"
BASE_IMAGE_URL = "https://langgraph-lesson-modifier.onrender.com/images/"

def generate_final_output(lesson_text: str, image_paths: list, audio_paths: list) -> dict:
    file_id = uuid.uuid4().hex
    txt_filename = f"final_lesson_{file_id}.txt"
    json_filename = f"final_lesson_{file_id}.json"
    md_filename = f"final_lesson_{file_id}.md"

    txt_path = os.path.join(FINAL_TXT_DIR, txt_filename)
    json_path = os.path.join(FINAL_JSON_DIR, json_filename)
    md_path = os.path.join(FINAL_MD_DIR, md_filename)

    # Valid file names from actual downloads
    valid_images = [os.path.basename(p) for p in image_paths]
    valid_audios = [os.path.basename(p) for p in audio_paths]

    # === TXT Output ===
    enriched_text = lesson_text
    for path in image_paths:
        fname = os.path.basename(path)
        enriched_text = enriched_text.replace(f"[IMAGE:{fname}]", f"\n🔍 [Insert Image: {fname}]\n")
    for path in audio_paths:
        fname = os.path.basename(path)
        enriched_text = enriched_text.replace(f"[AUDIO:{fname}]", f"\n🔊 [Insert Audio: {fname}]\n")

    with open(txt_path, "w") as f:
        f.write(enriched_text)

    # === Markdown Output ===
    md_lines = []
    lines = enriched_text.splitlines()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            md_lines.append("")
            continue

        # Markdown Formatting
        if stripped.lower().startswith("title:"):
            md_lines.append(f"# {stripped.replace('Title:', '').strip()}")
            continue
        elif "instructions" in stripped.lower():
            md_lines.append(f"## {stripped}")
            continue
        elif re.match(r"^\d+\.", stripped):
            md_lines.append(f"### {stripped}")
            continue
        elif stripped.endswith(":"):
            md_lines.append(f"**{stripped}**")
            continue

        # Audio
        audio_match = re.search(r"\[Insert Audio:\s*(.+?)\]", stripped)
        if audio_match:
            filename = audio_match.group(1).strip()
            if filename in valid_audios and filename.endswith(".mp3"):
                audio_url = f"{BASE_AUDIO_URL}{urllib.parse.quote(filename)}"
                md_lines.append(
                    f'<audio controls>\n  <source src="{audio_url}" type="audio/mpeg">\n  Your browser does not support the audio element.\n</audio>'
                )
            else:
                md_lines.append(f"<!-- Invalid audio reference: {filename} -->")
            continue

        # Image
        image_match = re.search(r"\[Insert Image:\s*(.+?)\]", stripped)
        if image_match:
            filename = image_match.group(1).strip()
            if filename in valid_images:
                image_url = f"{BASE_IMAGE_URL}{urllib.parse.quote(filename)}"
                md_lines.append(f"![Visual]({image_url})")
            else:
                md_lines.append(f"<!-- Invalid image reference: {filename} -->")
            continue

        # Plain text
        md_lines.append(stripped)

    with open(md_path, "w") as md:
        md.write("\n\n".join(md_lines))

    # === JSON Output ===
    blocks = []
    for line in lines:
        audio_match = re.search(r"\[Insert Audio:\s*(.+?)\]", line)
        if audio_match:
            fname = audio_match.group(1).strip()
            if fname in valid_audios:
                blocks.append({"type": "audio", "src": f"{BASE_AUDIO_URL}{urllib.parse.quote(fname)}"})
            continue

        image_match = re.search(r"\[Insert Image:\s*(.+?)\]", line)
        if image_match:
            fname = image_match.group(1).strip()
            if fname in valid_images:
                blocks.append({"type": "image", "src": f"{BASE_IMAGE_URL}{urllib.parse.quote(fname)}"})
            continue

        text_content = line.strip()
        if text_content:
            blocks.append({"type": "text", "content": text_content})

    with open(json_path, "w") as jf:
        json.dump(blocks, jf, ensure_ascii=False, indent=2)

    return {
        "txt_path": txt_path,
        "json_path": json_path,
        "md_path": md_path
    }