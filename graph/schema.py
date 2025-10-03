from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Union, Optional

class State(BaseModel):
    student_profile: Optional[Dict[str, Union[str, List[str]]]] = None
    rules: Optional[List[str]] = None
    lesson_url: Optional[HttpUrl] = None
    lesson_file_path: Optional[str] = None
    lesson_content: Optional[str] = None
    modified_lesson_text: Optional[str] = None
    audio_paths: Optional[List[str]] = None
    image_paths: Optional[List[str]] = None
    final_output_path: Optional[str] = None

    def get(self, key, default=None):
        return getattr(self, key, default)

    def update(self, updates: Dict[str, Union[str, List[str], List[Dict], None]]):
        for key, value in updates.items():
            setattr(self, key, value)
        return self