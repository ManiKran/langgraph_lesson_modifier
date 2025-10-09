# Updated main.py for Placeholder-based Lesson Editing

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
from typing import Dict, List, Union
import os
import uuid
import shutil

from tools.audio.generate import generate_audio_file
from tools.visuals.fetch import get_image_urls_from_serpapi, download_images
from graph.lesson_placeholder_graph import lesson_placeholders_app

app = FastAPI(title="Lesson Modifier API - Placeholder Based")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Request Models =====
class FullPipelineRequest(BaseModel):
    student_profile: Dict[str, Union[str, List[str]]]
    lesson_url: HttpUrl

class ModifyLessonRequest(BaseModel):
    rules: List[str]
    lesson_url: HttpUrl

class GenerateAudioRequest(BaseModel):
    prompt: str

# ===== Root Route =====
@app.get("/")
def root():
    return {"message": "Lesson Modifier API is running 🚀 (Placeholder Mode)"}

# ===== Full Pipeline: Placeholder only =====
@app.post("/full-pipeline")
async def full_pipeline(request: FullPipelineRequest):
    try:
        result = lesson_placeholders_app.invoke({
            "student_profile": request.student_profile,
            "lesson_url": str(request.lesson_url)
        })

        md_file = os.path.basename(result["final_output_md"])
        json_file = os.path.basename(result["final_output_json"])
        txt_file = os.path.basename(result["final_output_path"])

        return {
            "final_output_md": f"https://langgraph-lesson-modifier.onrender.com/markdown/{md_file}",
            "final_output_json": f"https://langgraph-lesson-modifier.onrender.com/json/{json_file}",
            "final_output_path": f"https://langgraph-lesson-modifier.onrender.com/files/{txt_file}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full pipeline failed: {str(e)}")

# ===== Image Search for Placeholder Replacement =====
@app.get("/api/search_images")
async def search_images(q: str = Query(...)):
    try:
        urls = get_image_urls_from_serpapi(q, count=5)
        return download_images(urls)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ===== Generate Audio on Demand =====
@app.post("/api/generate_audio")
async def generate_audio(request: GenerateAudioRequest):
    try:
        path = generate_audio_file(request.prompt)
        filename = os.path.basename(path)
        return {"audio_url": f"https://langgraph-lesson-modifier.onrender.com/audio/{filename}"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ===== Upload Audio =====
@app.post("/api/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        out_path = f"data/outputs/audio/{uuid.uuid4().hex}_{file.filename}"
        with open(out_path, "wb") as out_file:
            shutil.copyfileobj(file.file, out_file)
        filename = os.path.basename(out_path)
        return {"audio_url": f"https://langgraph-lesson-modifier.onrender.com/audio/{filename}"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ===== Upload Image =====
@app.post("/api/upload_image")
async def upload_image(file: UploadFile = File(...)):
    try:
        out_path = f"data/outputs/images/{uuid.uuid4().hex}_{file.filename}"
        with open(out_path, "wb") as out_file:
            shutil.copyfileobj(file.file, out_file)
        filename = os.path.basename(out_path)
        return {"image_url": f"https://langgraph-lesson-modifier.onrender.com/images/{filename}"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ===== Static File Routes =====
app.mount("/files", StaticFiles(directory="data/outputs/final"), name="files")
app.mount("/json", StaticFiles(directory="data/outputs/json"), name="json")
app.mount("/markdown", StaticFiles(directory="data/outputs/markdown"), name="markdown")
app.mount("/audio", StaticFiles(directory="data/outputs/audio"), name="audio")
app.mount("/images", StaticFiles(directory="data/outputs/images"), name="images")