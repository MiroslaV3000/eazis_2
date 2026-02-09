from fastapi import APIRouter

from src.project_objects import app


router = APIRouter(tags=["Анализатор языка текста"])



@router.get("/api/detect-language")
async def detect_language(url: str):
    return app.detect_language(url=url)

@router.post("/api/save")
async def create_chat(filename: str, results: dict):
    return app.save_results_to_file(filename=filename, results=results)


