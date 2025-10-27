import json
from fastapi import APIRouter, UploadFile, File
import os, shutil

from backend.config import UPLOAD_DIR
from backend.services.pdf_service import extract_text_from_pdf
from backend.services.llm_service import analyze_text_with_ai

router = APIRouter()
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze-pdf/")
async def analyze_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)
    ai_result = analyze_text_with_ai(text)

    return json.loads(ai_result)
