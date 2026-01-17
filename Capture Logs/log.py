import os
import io
import sys
from pyrogram import filters, Client
from pyrogram.types import Message

# --- IMPORT MAGIC ---
# This ensures Python looks in the ROOT folder for config/logger
# even though this file is deep inside MyselfNeon/modules/
sys.path.append(os.getcwd()) 

try:
    from config import OWNER_ID
    from logger import setup_logging
    
    # Enable logging logic immediately
    setup_logging()
    
except ImportError:
    print("⚠️ LOGGING ERROR: Could not find 'logger.py' or 'config.py' in Root.")
    OWNER_ID = 00000000

LOG_FILENAME = 'TELEGRAM_BOT.log'

@Client.on_message(filters.command('logs') & filters.user(OWNER_ID))
async def send_error_logs(bot, message: Message):
    try:
        if not os.path.exists(LOG_FILENAME):
            return await message.reply_text(
                "✅ **System Healthy**\nNo errors recorded on disk."
            )

        with open(LOG_FILENAME, 'rb') as f:
            log_data = f.read()

        if len(log_data) == 0:
            return await message.reply_text("ℹ️ **Log file is empty.**")

        virtual_file = io.BytesIO(log_data)
        virtual_file.name = "Error_Context_Log.txt"

        await message.reply_document(
            document=virtual_file,
            caption=(
                f"🚨 **Error Log Report**\n"
                f"**Size:** {len(log_data)} bytes\n"
                f"**Contains:** Errors + 20 lines of context before crash."
            )
        )

    except Exception as e:
        await message.reply_text(f"⚠️ **Error fetching logs:**\n`{str(e)}`")
