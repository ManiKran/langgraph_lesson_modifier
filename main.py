# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Union
import os

from graph.lesson_graph import lesson_app
from graph.short_lesson_graph import short_lesson_app

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Lesson Modification LangGraph API")


# test block:
import os
import openai

app = FastAPI()

@app.on_event("startup")
async def check_openai_key():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print("✅ Using OpenAI Key (partial):", openai.api_key[:5] + "..." + openai.api_key[-4:])
    try:
        # Optional: test if key is valid
        openai.Model.list()
        print("✅ OpenAI API key is valid")
    except Exception as e:
        print("❌ OpenAI API key error:", str(e))

# test block ends

# Enable CORS (Bubble or frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your Bubble domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request Models ----------
class FullPipelineRequest(BaseModel):
    student_profile: Dict[str, Union[str, List[str]]]
    lesson_url: HttpUrl

class ModifyLessonRequest(BaseModel):
    rules: List[str]
    lesson_url: HttpUrl

# ---------- Root Route ----------
@app.get("/")
def root():
    return {"message": "Lesson Modifier API is running 🚀"}

# ---------- Full Pipeline ----------
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

        txt_filename = os.path.basename(result["final_output_path"])
        json_filename = os.path.basename(result.get("final_output_json", ""))

        return {
            "image_paths": result["image_paths"],
            "audio_paths": result["audio_paths"],
            #"rules": result["rules"],
            "final_output_path": f"https://langgraph-lesson-modifier.onrender.com/files/{txt_filename}",
            "final_output_json": f"https://langgraph-lesson-modifier.onrender.com/json/{json_filename}" if json_filename else None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full pipeline failed: {str(e)}")

# ---------- Modify Lesson (Rules Only) ----------
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

# ---------- Static File Mounts ----------

# Final text files
app.mount(
    "/files",
    StaticFiles(directory="data/outputs/final"),
    name="files"
)

# Audio files
app.mount(
    "/audio",
    StaticFiles(directory="data/outputs/audio"),
    name="audio"
)

# Image files
app.mount(
    "/images",
    StaticFiles(directory="data/outputs/images"),
    name="images"
)

# Static mounts
app.mount("/json", StaticFiles(directory="data/outputs/json"), name="json")