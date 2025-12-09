# ------------------------------------------------
# File Name: Set_Commands.py
# Description: Auto Add Commands on new Deploys
# ------------------------------------------------

import asyncio
from pyrogram import Client
from pyrogram.types import BotCommand

# --- Edit This List ---
SET_COMMANDS = [
    ("start", "Check Alive Status"),
    ("alive", "Check Bot Latency"),
    ("help", "Get Usage Help")
]

# --- Internal Auto Sync Logic---
async def sync_bot_commands(app: Client):
    # 01. Wait for the Bot to Fully connect to Telegram Servers
    while not app.is_connected:
        await asyncio.sleep(1)

    print("Checking Command Sync...")

    try:
        # 02. --- Format the Commands ---
        commands = [BotCommand(cmd, desc) for cmd, desc in SET_COMMANDS]

        # 03. --- Push to Telegram ---
        await app.set_bot_commands(commands)
        
        print(f"✓ Commands Synced with Telegram: {SET_COMMANDS}")
    except Exception as e:
        print(f"✗ Failed to Sync Commands: {e}")

# ===================================
# PLUGIN ENTRY
# ===================================
def init(app: Client):
    # Instead of @app.on_start, we schedule a background task
    # This runs parallel to your bot starting up
    app.loop.create_task(sync_bot_commands(app))
