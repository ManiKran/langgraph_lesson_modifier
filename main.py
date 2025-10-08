# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Union
from fastapi.responses import JSONResponse
from tools.visuals.fetch import get_image_urls_from_serpapi, download_images
import os

from graph.lesson_graph import lesson_app
from graph.short_lesson_graph import short_lesson_app

from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Lesson Modification LangGraph API")

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

import uuid

processing_jobs = {}

# ---------- Full Pipeline ----------
from fastapi.responses import JSONResponse

@app.post("/full-pipeline")
@app.post("/full-pipeline/")
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
        md_filename = os.path.basename(result.get("final_output_md", ""))

        response_data = {
            "image_paths": result["image_paths"],
            "audio_paths": result["audio_paths"],
            "final_output_path": f"https://langgraph-lesson-modifier.onrender.com/files/{txt_filename}",
            "final_output_json": f"https://langgraph-lesson-modifier.onrender.com/json/{json_filename}" if json_filename else None,
            "final_output_md": f"https://langgraph-lesson-modifier.onrender.com/markdown/{md_filename}" if md_filename else None
        }

        return JSONResponse(content=response_data)

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
    
# ---------- Seaarch Images in Preview ----------
from fastapi import Query

@app.get("/api/search_images")
async def search_images(q: str = Query(..., description="Search query")):
    """
    Search for images using SerpAPI and return public URLs.
    """
    try:
        if not q:
            return JSONResponse(status_code=400, content={"error": "Missing query parameter 'q'"})
        
        urls = get_image_urls_from_serpapi(query=q, count=5)
        public_urls = download_images(urls)
        return public_urls
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

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

# Markdown files
app.mount(
    "/markdown",
    StaticFiles(directory="data/outputs/markdown"),
    name="markdown"
)