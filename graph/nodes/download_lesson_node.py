# graph/nodes/download_lesson_node.py

from utils.file_utils import download_file
from utils.file_parser import extract_text_from_file

def download_lesson_node(state: dict) -> dict:
    """
    Downloads the lesson file from URL and extracts its text content.
    """
    print("[DownloadLessonNode] Downloading lesson...")
    lesson_url = state.get("lesson_url")
    if not lesson_url:
        raise ValueError("Missing lesson_url in state.")

    # ✅ Cast to string to avoid decode error
    file_path = download_file(str(lesson_url))
    lesson_content = extract_text_from_file(file_path)

    print(file_path)
    print(lesson_content[:500])  # Print first 500 characters for verification

    state.update({
        "lesson_file_path": file_path,
        "lesson_content": lesson_content
    })
    return state