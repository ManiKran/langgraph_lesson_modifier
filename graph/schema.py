# graph/schema.py

from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Union, Optional

class State(BaseModel):
    """
    This defines the state that moves through your LangGraph pipeline.
    Each node in the graph can read/write any of these fields.
    """
    student_profile: Optional[Dict[str, Union[str, List[str]]]] = None
    rules: Optional[List[str]] = None
    lesson_url: Optional[HttpUrl] = None
    lesson_path: Optional[str] = None  # local file path after download
    lesson_content: Optional[str] = None  # extracted raw text
    modified_lesson_text: Optional[str] = None  # final modified text with placeholders
    audios: Optional[List[str]] = None  # local paths to generated audio files
    images: Optional[List[str]] = None  # local paths to downloaded images