from pathlib import Path

BASE_DIR = Path(__name__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR/"uploads"
UPLOAD_DIR.mkdir(exist_ok=True)