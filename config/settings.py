import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID", "0"))
API_HASH = os.getenv("TELEGRAM_API_HASH", "")
SESSION_NAME = os.getenv("TELEGRAM_SESSION_NAME", "session")
KEYWORDS = [kw.strip() for kw in os.getenv("KEYWORDS", "").split(",") if kw.strip()]
TARGET_CHANNEL_IDS = [int(cid.strip()) for cid in os.getenv("TARGET_CHANNEL_IDS", "").split(",") if cid.strip()]
