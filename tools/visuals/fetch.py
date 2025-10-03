# tools/visuals/fetch.py

import os
import uuid
import requests
from typing import List, Tuple
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

IMAGE_OUTPUT_DIR = "data/outputs/images"
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def get_image_urls_from_unsplash(query: str, count: int = 1) -> List[str]:
    """
    Fetch image URLs from Unsplash based on a query.
    """
    headers = {"Accept-Version": "v1"}
    url = f"https://api.unsplash.com/photos/random?query={query}&count={count}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url, headers=headers)

    try:
        data = response.json()
        if isinstance(data, list):
            return [item["urls"]["regular"] for item in data]
        else:
            return []
    except:
        return []

def download_images(image_urls: List[str]) -> List[str]:
    """
    Downloads image URLs to local disk and returns file paths.
    """
    local_paths = []
    for url in image_urls:
        try:
            img_data = requests.get(url).content
            filename = f"image_{uuid.uuid4().hex}.jpg"
            path = os.path.join(IMAGE_OUTPUT_DIR, filename)
            with open(path, "wb") as f:
                f.write(img_data)
            local_paths.append(path)
        except Exception as e:
            print(f"[VisualAgent] Failed to download image: {e}")
    return local_paths