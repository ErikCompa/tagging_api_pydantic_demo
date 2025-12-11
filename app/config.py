import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing from environment variables")

GOOGLE_VISION_BASE_URL = "https://vision.googleapis.com/v1/images:annotate"
GOOGLE_VISION_URL = f"{GOOGLE_VISION_BASE_URL}?key={GOOGLE_API_KEY}"
