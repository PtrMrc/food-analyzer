import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os, shutil

from backend.config import UPLOAD_DIR
from backend.services.pdf_service import extract_text_from_pdf
from backend.services.llm_service import analyze_text_with_ai

router = APIRouter()
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024

@router.post("/analyze-pdf/")
async def analyze_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Csak PDF fájlok engedélyezettek!")

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="A fájl túl nagy! Maximum 10MB engedélyezett.")

    if file_size == 0:
        raise HTTPException(status_code=400, detail="A fájl üres!")

    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = extract_text_from_pdf(file_path)

        if not text or len(text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Nem sikerült szöveget kinyerni a PDF-ből!")

        ai_result = analyze_text_with_ai(text)
        result_data = json.loads(ai_result)

        if os.path.exists(file_path):
            os.remove(file_path)

        return JSONResponse(content=result_data)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Hibás válasz az AI-tól")
    except Exception as e:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Hiba történt: {str(e)}")