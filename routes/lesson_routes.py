# routes/lesson_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import HttpUrl
from typing import Dict, Union, List
from graph.lesson_graph import lesson_app

router = APIRouter()

@router.post("/modify-lesson/")
async def modify_lesson(
    student_profile: Dict[str, Union[str, List[str]]],
    lesson_url: HttpUrl,
):
    try:
        # Input to the LangGraph pipeline
        inputs = {
            "student_profile": student_profile,
            "lesson_url": str(lesson_url),
        }

        # Run the LangGraph lesson modifier
        result = lesson_app.invoke(inputs)

        return {
            "modified_lesson": result.get("modified_lesson"),
            "audios": result.get("audios", []),
            "images": result.get("images", []),
            "rules_applied": result.get("rules", []),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))