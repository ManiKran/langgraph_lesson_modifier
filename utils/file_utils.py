# utils/file_utils.py

import os
import uuid
import requests
from urllib.parse import urlparse

def download_file(url: str, dest_dir: str = "data/inputs") -> str:
    """
    Downloads a file from the given URL and stores it in the destination directory.
    Returns the full path of the downloaded file.
    """
    os.makedirs(dest_dir, exist_ok=True)

    # Extract filename or generate one
    parsed_url = urlparse(url)
    original_name = os.path.basename(parsed_url.path)
    ext = os.path.splitext(original_name)[1] or ".bin"
    unique_filename = f"{uuid.uuid4().hex}{ext}"

    file_path = os.path.join(dest_dir, unique_filename)

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

        return file_path

    except Exception as e:
        raise RuntimeError(f"Failed to download file: {url} — {str(e)}")