from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from routes import pdf_routes

# Initialize app
app = FastAPI(
    title="PDF AI Extractor",
    description="Extract allergens and nutrition data from PDFs"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "http://127.0.0.1:5173",
        "https://*.netlify.app", 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf_routes.router)

@app.get("/")
def root():
    return {"status": "ok", "upload_dir": UPLOAD_DIR}
