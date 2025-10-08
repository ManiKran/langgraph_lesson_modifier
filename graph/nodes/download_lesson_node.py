# graph/nodes/download_lesson_node.py

from utils.file_utils import download_file
from utils.file_parser import extract_text_from_file

def download_lesson_node(state: dict) -> dict:
    """
    Downloads the lesson file from URL and extracts its text content.
    """
    lesson_url = state.get("lesson_url")
    if not lesson_url:
        raise ValueError("Missing lesson_url in state.")

    # ✅ Cast to string to avoid decode error
    file_path = download_file(str(lesson_url))
    lesson_content = extract_text_from_file(file_path)

    state.update({
        "lesson_file_path": file_path,
        "lesson_content": lesson_content
    })
    return state