from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Union, Optional


class State(BaseModel):
    student_profile: Optional[Dict[str, Union[str, List[str]]]] = None
    rules: Optional[List[str]] = None
    lesson_url: Optional[HttpUrl] = None
    lesson_path: Optional[str] = None
    lesson_content: Optional[str] = None
    modified_lesson_text: Optional[str] = None
    audios: Optional[List[str]] = None
    images: Optional[List[str]] = None

    def get(self, key, default=None):
        return getattr(self, key, default)