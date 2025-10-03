# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Union

from graph.lesson_graph import lesson_app
from graph.short_lesson_graph import short_lesson_app

app = FastAPI(title="Lesson Modification LangGraph API")

# Enable CORS (Bubble or frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your Bubble frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request models for API endpoints
class FullPipelineRequest(BaseModel):
    student_profile: Dict[str, Union[str, List[str]]]
    lesson_url: HttpUrl

class ModifyLessonRequest(BaseModel):
    rules: List[str]
    lesson_url: HttpUrl

@app.get("/")
def root():
    return {"message": "Lesson Modifier API is running 🚀"}

@app.post("/full-pipeline")
async def full_pipeline(request: FullPipelineRequest):
    """
    Full pipeline: Generate rules from student profile → Download lesson → Modify → Add audio/visuals → Output.
    """
    try:
        result = lesson_app.invoke({
            "student_profile": request.student_profile,
            "lesson_url": str(request.lesson_url)
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full pipeline failed: {str(e)}")

@app.post("/modify-lesson")
async def modify_lesson_with_rules(request: ModifyLessonRequest):
    """
    Short pipeline: Use existing rules → Download lesson → Modify → Add audio/visuals → Output.
    """
    try:
        result = short_lesson_app.invoke({
            "rules": request.rules,
            "lesson_url": str(request.lesson_url)
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lesson modification failed: {str(e)}")