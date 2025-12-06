# ------------------------------------------------
# File Name: Config.py
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# Last Modified: 2025-12-04 (Refactored for DB Storage)
# ------------------------------------------------

import os
from dotenv import load_dotenv

load_dotenv()

# --- Telegram Credentials ---
API_ID = int(os.getenv("API_ID", 0)) 
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# --- Authorization Config ---
OWNER_ID = int(os.getenv("OWNER_ID", 841851780)) 

# --- Database Config (MongoDB) ---
DB_URI = os.getenv("DB_URI", "")
DB_NAME = os.getenv("DB_NAME", "PMT-Testing")

# --- Application Config ---
# Check interval range in seconds
MIN_CHECK_INTERVAL = int(os.getenv("MIN_CHECK_INTERVAL", 8))
MAX_CHECK_INTERVAL = int(os.getenv("MAX_CHECK_INTERVAL", 12))

# Server Port (Required for cloud deployments)
PORT = int(os.getenv("PORT", 8080))
