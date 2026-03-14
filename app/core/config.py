from pathlib import Path
from dot_env import load_dotenv

load_dotenv()

BASE_DIR = Path(__name__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR/"uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")