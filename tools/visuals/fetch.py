# tools/visuals/fetch.py

import os
import uuid
import requests
from serpapi import GoogleSearch
from typing import List

IMAGE_OUTPUT_DIR = "data/outputs/images"
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

BASE_IMAGE_URL = "https://langgraph-lesson-modifier.onrender.com/images/"

def get_image_urls_from_serpapi(query: str, count: int = 1) -> List[str]:
    """
    Fetch image URLs from Google Images using SerpAPI.
    """
    try:
        params = {
            "q": query,
            "tbm": "isch",
            "api_key": SERPAPI_KEY,
            "num": count
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        if "images_results" in results:
            urls = [img["original"] for img in results["images_results"][:count]]
            print(f"[SerpAPI] Fetched {len(urls)} image URLs for '{query}'")
            return urls
        else:
            print("[SerpAPI] No image results found.")
            return []
    except Exception as e:
        print(f"[SerpAPI] Error fetching images: {e}")
        return []

def download_images(image_urls: List[str]) -> List[str]:
    """
    Downloads image URLs to local disk and returns public URLs.
    """
    local_paths = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in image_urls:
        try:
            print(f"[Download] Attempting: {url}")
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(f"[Download] Failed: {response.status_code}")
                continue

            filename = f"image_{uuid.uuid4().hex}.jpg"
            path = os.path.join(IMAGE_OUTPUT_DIR, filename)

            with open(path, "wb") as f:
                f.write(response.content)

            print(f"[Download] Saved: {path}")
            local_paths.append(f"{BASE_IMAGE_URL}{filename}")

        except Exception as e:
            print(f"[Download] Error: {e}")

    return local_paths