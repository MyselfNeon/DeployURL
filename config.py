# ------------------------------------------------
# File Name: config.py
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# Last Modified: 2025-12-06 (Multi-Owner Support)
# ------------------------------------------------

import os
from dotenv import load_dotenv

load_dotenv()

# --- Telegram Credentials ---
API_ID = int(os.getenv("API_ID", 0)) 
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# --- Authorization Config ---
# Parse Comma-Separated IDs (e.g. "12345, 67890")
raw_owner_ids = os.getenv("OWNER_ID", "841851780,7430064956")
try:
    # Split by comma, strip spaces, and ensure they are numbers
    OWNER_IDS = {int(x) for x in raw_owner_ids.split(",") if x.strip().isdigit()}
except Exception as e:
    print(f"Error parsing OWNER_ID: {e}")
    OWNER_IDS = set()

# --- Database Config (MongoDB) ---
DB_URI = os.getenv("DB_URI", "")
DB_NAME = os.getenv("DB_NAME", "PMT-Testing")

# --- Application Config ---
# Check interval range in seconds (Default: 8 to 12 seconds)
MIN_CHECK_INTERVAL = int(os.getenv("MIN_CHECK_INTERVAL", 8))
MAX_CHECK_INTERVAL = int(os.getenv("MAX_CHECK_INTERVAL", 12))

# Server Port (Required for cloud deployments)
PORT = int(os.getenv("PORT", 8080))
