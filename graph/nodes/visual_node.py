# graph/nodes/visual_node.py

from tools.visuals.fetch import get_image_urls_from_unsplash, download_images
from openai import OpenAI
import os, ast, re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def extract_image_queries(text: str, rules: list) -> list:
    """
    Use LLM to suggest what image topics should be added to the lesson.
    """
    if not any("visual" in rule.lower() for rule in rules):
        return []

    prompt = f"""
You are an assistant that helps make lesson plans more visual and engaging.

Lesson:
{text}

Rules:
{rules}

Extract a list of 3–5 visual elements that should be added to this lesson. Return them as a Python list of strings.

Visual Suggestions:
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )

    raw = response.choices[0].message.content.strip()
    try:
        queries = ast.literal_eval(raw)
        return queries if isinstance(queries, list) else []
    except:
        return []


def visual_node(state: dict) -> dict:
    """
    Adds visual aids to the lesson content based on rules and lesson structure.
    Replaces existing [Insert Image: ...] tags with downloaded images.
    """
    text = state.get("modified_lesson_text", "")
    rules = state.get("rules", [])

    if not text or not rules:
        return state

    # Step 1: Extract image queries using GPT
    queries = extract_image_queries(text, rules)
    image_urls = []
    for query in queries:
        image_urls.extend(get_image_urls_from_unsplash(query, count=1))

    image_paths = download_images(image_urls)

    # Step 2: Replace existing [Insert Image: ...] with [IMAGE:filename]
    def replace_placeholder(match, filenames=image_paths):
        if filenames:
            path = filenames.pop(0)
            return f"[IMAGE:{os.path.basename(path)}]"
        else:
            return match.group(0)  # fallback: leave original

    pattern = r"\[Insert Image:.*?\]"
    text = re.sub(pattern, replace_placeholder, text)

    # Step 3: If extra images left, append at end
    for path in image_paths:
        text += f"\n\n[IMAGE:{os.path.basename(path)}]"

    state.update({
        "modified_lesson_text": text,
        "image_paths": image_paths
    })
    return state