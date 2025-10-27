import pdfplumber
import pytesseract
from pdf2image import convert_from_path

def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    # Try reading with pdfplumber
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
    except Exception as e:
        print("pdfplumber error:", e)

    # OCR fallback if no text found
    if not text.strip():
        print("No text found, using OCR...")
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text.strip()
