# ------------------------------------------------
# File Name: Useless.py
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# Last Modified: 2025-10-21
# ------------------------------------------------

import os
import sys
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from MyselfNeon.db import db
from config import OWNER_ID 

logger = logging.getLogger(__name__)

# Key to store restart message ID so we can delete it after reboot
RESTART_MSG_KEY = "restart_message_info"

def register_useless_commands(bot, verify_auth_func):
    """
    Registers system commands.
    """

    @bot.on_message(filters.command("restart"))
    async def restart_cmd(client: Client, message: Message):
        
        # --- STRICT SECURITY CHECK ---
        if message.from_user.id != OWNER_ID:
            try:
                # 1. Send Sticker
                m = await message.reply_sticker("CAACAgIAAxkBAAJF4WkjF7pMqaiigSJbxdN2p5iDrzjFAAJ-GgACglXYSXgCrotQHjibHgQ")
                await asyncio.sleep(1)
                await m.delete()
            except: pass
            
            # 2. Send Text
            await message.reply("⛔ **__ACCESS DENIED__** ⛔\n\n__Only the Bot Owner can restart the server.__")
            return

        # Send "Restarting" message
        restart_message = await message.reply_text("🔄 **__Restarting Bot...__**\n\n__Reloading scripts and reconnecting...__")
        
        try:
            logger.info(f"Owner {message.from_user.id} triggered bot restart.")
            
            # Save the message ID to DB
            await db.set_state(RESTART_MSG_KEY, {
                "chat_id": restart_message.chat.id,
                "message_id": restart_message.id,
            })
            
            await asyncio.sleep(1)
            # Restart the process
            os.execlp(sys.executable, sys.executable, *sys.argv)
            
        except Exception as e:
            logger.error(f"Failed to execute restart: {e}")
            await restart_message.edit_text(f"❌ **__Restart Failed: {e}__**")

    logger.info("Restart command registered.")
