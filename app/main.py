from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Config
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize app
app = FastAPI(
    title="PDF AI Extractor",
    description="Extract allergens and nutrition data from PDFs"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: limit later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
from app.routes import pdf_routes
app.include_router(pdf_routes.router)

@app.get("/")
def root():
    return {"status": "ok", "upload_dir": UPLOAD_DIR}
