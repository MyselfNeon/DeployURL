# ------------------------------------------------
# File Name: main.py
# Description: Core Logic (Session, Loop, Checks)
# ------------------------------------------------

import asyncio
import logging
import random
import datetime 
import aiohttp 
from curl_cffi.requests import AsyncSession
from pyrogram import Client, filters
from pyrogram.types import Message

# UPDATED IMPORT: OWNER_IDS
from config import API_ID, API_HASH, BOT_TOKEN, MIN_CHECK_INTERVAL, MAX_CHECK_INTERVAL, PORT, OWNER_IDS
from app import start_web_server

# Import Logic
from MyselfNeon.track import check_user_status, check_forums
from MyselfNeon.useless import register_useless_commands, RESTART_MSG_KEY
from MyselfNeon.db import db

# YOUR KEEP ALIVE URL HERE
KEEP_ALIVE_URL = "https://website-monitor-ddy2.onrender.com/" 

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global flag
BOT_READY_MESSAGE_SENT = False

# Supported Reactions
REACTIONS = ["🤝", "👍", "⚡️", "🫡", "🔥", "😎", "✅"]

# --- ADVANCED BROWSER CONFIGURATIONS ---
BROWSER_CONFIGS = [
    {
        "impersonate": "chrome120",
        "headers": {
            "Referer": "https://www.google.com/",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        }
    },
    {
        "impersonate": "chrome110",
        "headers": {
            "Referer": "https://www.google.com/",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="110", "Google Chrome";v="110"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Upgrade-Insecure-Requests": "1",
        }
    },
    {
        "impersonate": "edge101",
        "headers": {
            "Referer": "https://www.bing.com/",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Ch-Ua": '" Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
        }
    },
    {
        "impersonate": "safari17_0",
        "headers": {
            "Referer": "https://www.google.com/",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
        }
    }
]

# Initialize Pyrogram Client
bot = Client(
    "platinmods_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- General Authorization Helper (Owner + Auth Users) ---
async def verify_authorization(message):
    if not message.from_user: return False
    # CHECK SET OF IDS
    if message.from_user.id in OWNER_IDS: return True
    if await db.is_user_authorized(message.from_user.id): return True

    try:
        # Access Denied Sticker 
        m = await message.reply_sticker("CAACAgIAAxkBAAJF4WkjF7pMqaiigSJbxdN2p5iDrzjFAAJ-GgACglXYSXgCrotQHjibHgQ")
        await asyncio.sleep(1) 
        await m.delete() 
    except: pass

    await message.reply("⛔ **__ACCESS DENIED__** ⛔\n\n__You are not authorized to use this command.__")
    return False

# --- START COMMAND ---
@bot.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    try: await message.react(emoji=random.choice(REACTIONS), big=True)
    except: pass
    try:
        m = await message.reply_sticker("CAACAgIAAxkBAAJF62kjGL73G1GeWXTazcwPE0kEwIwfAAKOFQACJU3BSY8WTX7r0TbzHgQ")
        await asyncio.sleep(1)
        await m.delete()
    except: pass
    
    chat_type = message.chat.type.name.lower()
    if chat_type == 'private':
        reply_text = f"👋 **__Bot is Online !!__**\n\n__**Your Unique User ID is:__** `{message.chat.id}`\n\n**__Action Required: Send this ID to the Owner to get authorized.__**"
    else:
         reply_text = f"👋 **__Bot is Online !!__**\n\n**__The Chat ID for this {chat_type.upper()} is:__** `{message.chat.id}`"
    await message.reply(reply_text)

# --- CHECK COMMAND ---
@bot.on_message(filters.command("check"))
async def force_check(client, message):
    if not await verify_authorization(message): return
    
    # Loading Sticker
    tmp = await message.reply_sticker("CAACAgEAAxkBAAJHQWkqZs4YE4Oxlil7LNLgruuoGkkaAAItAgACpyMhRD1AMMntg7S2HgQ")
    
    try:
        config = random.choice(BROWSER_CONFIGS)
        
        async with AsyncSession(
            timeout=20.0, 
            impersonate=config['impersonate'], 
            headers=config['headers']
        ) as http_client:
            user_status_data = await check_user_status(http_client, client)
            forum_counts = await check_forums(http_client, client)
        
        summary_parts = ["✅ **__Manual Check Completed__**\n", "👤 **__User Status__**"]
        
        for name, info in user_status_data.items():
            status = info.get("status", "Unknown")
            
            # --- TIME FIX LOGIC (Strict IST Conversion) ---
            display_time = info.get("last_seen", "Unknown")
            
            if status != "Online":
                db_time = await db.get_last_seen(name)
                if db_time:
                    try:
                        # 1. Ensure db_time is treated as UTC (Mongo Default)
                        if db_time.tzinfo is None:
                            utc_time = db_time.replace(tzinfo=datetime.timezone.utc)
                        else:
                            utc_time = db_time.astimezone(datetime.timezone.utc)

                        # 2. Convert to IST (UTC + 5:30)
                        ist_tz = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
                        ist_time = utc_time.astimezone(ist_tz)
                        
                        # 3. Format
                        display_time = ist_time.strftime("%d %b, %I:%M %p (IST)")
                    except Exception as time_err:
                        logger.error(f"Time conversion error: {time_err}")
                        display_time = str(db_time) # Fallback
            else:
                display_time = "Online Now"
            # -------------------------------------------------

            emoji = "🟢" if status == "Online" else "🔴" if status == "Offline" else "❓"
            summary_parts.append(f"__• {name}: **{status}** {emoji}__\n   __Last seen: {display_time}__")
        
        summary_parts.append("\n📚 **__Forum Thread Counts__**")
        for forum, count in forum_counts.items():
            summary_parts.append(f"__• {forum}: **{count} threads__**")
        
        await client.send_message(message.chat.id, "\n".join(summary_parts))
        await tmp.delete()
    
    except Exception as e:
        logger.error(f"Error during force check: {e}")
        await message.reply(f"❌ **__Check failed.__**\n\n__{e}__")

# --- Scheduler ---
async def scheduler():
    global BOT_READY_MESSAGE_SENT
    while not bot.is_connected:
        logger.info("Scheduler waiting for Telegram client to start...")
        await asyncio.sleep(5)
        
    if not BOT_READY_MESSAGE_SENT:
        restart_info = await db.get_state(RESTART_MSG_KEY)
        if restart_info:
            try:
                await bot.delete_messages(restart_info['chat_id'], restart_info['message_id'])
                await db.set_state(RESTART_MSG_KEY, None)
            except: pass
            
        # NOTIFY ALL OWNERS + AUTH USERS
        recipients = set(await db.get_all_auth_users())
        recipients.update(OWNER_IDS)
        
        for uid in recipients:
            try: await bot.send_message(uid, "✅ **__Bot Online & Monitoring__**")
            except: pass
        BOT_READY_MESSAGE_SENT = True
            
    while True:
        # 1. Pick a new browser identity for this session
        config = random.choice(BROWSER_CONFIGS)
        logger.info(f"Starting new session with: {config['impersonate']}")
        
        # 2. RETENTION: Decide how long to keep this session (5 to 10 checks)
        session_life_cycles = random.randint(5, 10)

        try:
            # Create Session with Headers and Impersonation (NO PROXY)
            async with AsyncSession(
                timeout=20.0, 
                impersonate=config['impersonate'], 
                headers=config['headers']
            ) as http_client:
                
                for i in range(session_life_cycles):
                    await check_user_status(http_client, bot)
                    await check_forums(http_client, bot)
                    
                    # Sleep between checks inside the same session
                    await asyncio.sleep(random.randint(MIN_CHECK_INTERVAL, MAX_CHECK_INTERVAL))
                    
        except Exception as e:
            logger.error(f"Scheduler Session Error: {e}")
            # --- SMART BACKOFF: COOL DOWN ON ERROR ---
            # If we crashed (403/Connection Error), wait longer (60-120s)
            logger.warning("⚠️ Error detected. Cooling down for 60-120s...")
            await asyncio.sleep(random.randint(60, 120))

# --- Keep-Alive ---
async def keep_alive():
    if not KEEP_ALIVE_URL: return
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(KEEP_ALIVE_URL) as resp:
                    if resp.status != 200: logger.warning(f"Keep-alive status {resp.status}")
            except Exception as e: logger.error(f"Keep-alive failed: {e}")
            await asyncio.sleep(300)

if __name__ == "__main__":
    logger.info(f"Starting Web Server on port {PORT}")
    start_web_server(PORT)
    logger.info("Registering Bot Plugins...")
    # Register the commands moved to useless.py
    register_useless_commands(bot)
    logger.info("Starting Telegram Bot...")
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    if KEEP_ALIVE_URL: loop.create_task(keep_alive())
    bot.run()
