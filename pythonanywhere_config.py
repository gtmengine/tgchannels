import os
from pathlib import Path

# Set up paths for PythonAnywhere
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "db.sqlite")

# Ensure the database directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Environment variables (you'll need to set these in PythonAnywhere's web interface)
BOT_TOKEN = os.getenv("BOT_TOKEN", "7735328862:AAFrcBtnZEmL9O-kM0dZ2Y_yDoFh11ICm40")
API_ID = os.getenv("API_ID", "")  # You'll need to set this
API_HASH = os.getenv("API_HASH", "")  # You'll need to set this
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]  # You'll need to set this
FEEDBACK_FORM = os.getenv("FEEDBACK_FORM", "")  # Optional 