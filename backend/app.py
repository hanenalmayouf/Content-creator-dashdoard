import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

# Import generator functions
from generator import generate_syllabus_ai, build_lesson

# Load environment variables
load_dotenv()

app = FastAPI(
    title="منصة توليد المناهج والدروس التفاعلية",
    description="FastAPI Backend for AI-powered syllabus planner and lesson generator",
    version="1.0.0"
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ensure generated_lessons directory exists
GENERATED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_lessons")
os.makedirs(GENERATED_DIR, exist_ok=True)

# Mount generated lessons as static files
app.mount("/lessons", StaticFiles(directory=GENERATED_DIR), name="lessons")

# Request/Response schemas
class SyllabusRequest(BaseModel):
    topic: str = Field(..., example="أساسيات بايثون")
    hours_per_day: int = Field(default=4, ge=1, le=12)
    days_per_week: int = Field(default=3, ge=1, le=7)
    weeks_count: int = Field(default=2, ge=1, le=52)
    strategies: str = Field(default="التعلم القائم على المشاريع، التلعيب والمسابقات")
    target_audience: str = Field(default="المتخصصون (علوم حاسب أو ذكاء اصطناعي)")

class LessonRequest(BaseModel):
    lesson_id: str = Field(..., example="w1d1")
    lesson_title: str = Field(..., example="مقدمة في لغة بايثون")
    lesson_desc: str = Field(..., example="التعرف على بناء الجمل البرمجية والمتغيرات.")
    objectives: List[str] = Field(default=[])
    course_title: str = Field(default="دورة تدريبية")
    strategies: List[str] = Field(default=[])
    strategy_application: str = Field(default="")

class SaveFileRequest(BaseModel):
    lesson_id: str
    file_type: str = "qmd"
    content: str

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "FastAPI backend for Interactive Lesson Generator is running.",
        "endpoints": {
            "root": "/",
            "lessons_static": "/lessons",
            "generate_syllabus": "/api/generate-syllabus (POST)",
            "generate_lesson": "/api/generate-lesson (POST)",
            "load_lesson_file": "/api/load-lesson-file (GET)",
            "save_lesson_file": "/api/save-lesson-file (POST)"
        }
    }

@app.post("/api/generate-syllabus")
async def generate_syllabus(req: SyllabusRequest):
    try:
        syllabus = generate_syllabus_ai(
            topic=req.topic,
            hours_per_day=req.hours_per_day,
            days_per_week=req.days_per_week,
            weeks_count=req.weeks_count,
            strategies=req.strategies,
            target_audience=req.target_audience
        )
        return syllabus
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate syllabus: {str(e)}")

@app.post("/api/generate-lesson")
async def generate_lesson(req: LessonRequest):
    try:
        result = build_lesson(
            lesson_id=req.lesson_id,
            lesson_title=req.lesson_title,
            lesson_desc=req.lesson_desc,
            objectives=req.objectives,
            course_title=req.course_title,
            strategies=req.strategies,
            strategy_application=req.strategy_application
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate lesson: {str(e)}")

@app.get("/api/load-lesson-file")
def load_lesson_file(lesson_id: str, file_type: str = "qmd"):
    try:
        if file_type != "qmd":
            raise HTTPException(status_code=400, detail="Only 'qmd' file type is supported for editing currently.")
        
        qmd_path = os.path.join(GENERATED_DIR, lesson_id, "lesson.qmd")
        if not os.path.exists(qmd_path):
            raise HTTPException(status_code=404, detail=f"Lesson file not found for lesson ID: {lesson_id}")
        
        with open(qmd_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return {"lesson_id": lesson_id, "file_type": file_type, "content": content}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load file: {str(e)}")

@app.post("/api/save-lesson-file")
async def save_lesson_file(req: SaveFileRequest):
    try:
        if req.file_type != "qmd":
            raise HTTPException(status_code=400, detail="Only 'qmd' file type is supported currently.")
        
        from generator import recompile_lesson_slides
        result = recompile_lesson_slides(req.lesson_id, req.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save and recompile: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

