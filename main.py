from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import Dict, List, Union, Optional
from pydantic import HttpUrl
from fastapi.middleware.cors import CORSMiddleware
from graph.lesson_graph import lesson_app
from graph.short_lesson_graph import short_lesson_app

app = FastAPI(title="Lesson Modification LangGraph API")

# Optional: Enable CORS for Bubble or frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with Bubble frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/full-pipeline")
async def full_pipeline(
    student_profile: Dict[str, Union[str, List[str]]],
    lesson_url: HttpUrl,
):
    """
    Full pipeline: Generate rules from student profile → Download lesson → Modify → Add audio/visuals → Output.
    """
    try:
        result = lesson_app.invoke({
            "student_profile": student_profile,
            "lesson_url": str(lesson_url)
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full pipeline failed: {str(e)}")


@app.post("/modify-lesson")
async def modify_lesson_with_rules(
    rules: List[str],
    lesson_url: HttpUrl,
):
    """
    Short pipeline: Use existing rules → Download lesson → Modify → Add audio/visuals → Output.
    """
    try:
        result = short_lesson_app.invoke({
            "rules": rules,
            "lesson_url": str(lesson_url)
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lesson modification failed: {str(e)}")