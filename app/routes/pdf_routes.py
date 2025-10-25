from fastapi import APIRouter, File, UploadFile
import shutil
import os
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

router = APIRouter(prefix="/pdf", tags=["PDF"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "message": "PDF uploaded successfully"}

@router.post("/extract/")
async def extract_text(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = ""

    # Try text extraction
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print("pdfplumber error:", e)

    # Fallback to OCR
    if not text.strip():
        print("No text found, running OCR...")
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img)

    return {
        "filename": file.filename,
        "text_preview": text[:1000],
        "text_length": len(text)
    }