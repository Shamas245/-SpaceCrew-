from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    NASA_API_KEY = os.getenv("NASA_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    LAUNCH_LIBRARY_BASE_URL = "https://ll.thespacedevs.com/2.2.0"
    OPEN_NOTIFY_BASE_URL = "http://api.open-notify.org"