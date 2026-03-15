from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

BASE_DIR = Path(__name__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR/"uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

VECTOR_STORE_DIR = BASE_DIR/"vector_store"
VECTOR_STORE_DIR.mkdir(exist_ok=True)