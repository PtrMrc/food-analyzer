import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")