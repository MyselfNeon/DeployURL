import random
import string
import requests
import aiohttp
from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from MyselfNeon import app
from MyselfNeon.core.func import *
from config import MONGO_DB, WEBSITE_URL, AD_API, LOG_GROUP

# --- DATABASE & GLOBALS ---
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]

Param = {}

# --- HELPER FUNCTIONS ---
async def create_ttl_index():
    """Create a Time-To-Live index for tokens."""
    await token.create_index("expires_at", expireAfterSeconds=0)

async def generate_random_param(length=8):
    """Generate a random parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def get_shortened_url(deep_link):
    """Shorten the deep link using the external API."""
    api_url = f"https://{WEBSITE_URL}/api?api={AD_API}&url={deep_link}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()   
                if data.get("status") == "success":
                    return data.get("shortenedUrl")
    return None

async def is_user_verified(user_id):
    """Check if a user has an active session."""
    session = await token.find_one({"user_id": user_id})
    return session is not None

# --- HANDLERS ---
@app.on_message(filters.command("start"))
async def token_handler(client, message):
    """Handle the /start command."""
    join = await subscribe(client, message)
    if join == 1:
        return

    chat_id = "neonfiles"
    user_id = message.chat.id
    
    # Handle basic /start without parameters
    if len(message.command) <= 1:
        msg = await app.get_messages(chat_id, 30)
        image_url = "https://i.postimg.cc/v8q8kGyz/startimg-1.jpg"
        
        join_button = InlineKeyboardButton("Join Channel", url="https://t.me/team_spy_pro")
        premium = InlineKeyboardButton("Get Premium", url="https://t.me/kingofpatal")   
        
        keyboard = InlineKeyboardMarkup([
            [join_button],   
            [premium]    
        ])
        
        await message.reply_photo(
            msg.photo.file_id,
            caption=(
                "Hi 👋 Welcome, Wanna intro...?\n\n"
                "✳️ I can save posts from channels or groups where forwarding is off. "
                "I can download videos/audio from YT, INSTA, ... social platforms\n"
                "✳️ Simply send the post link of a public channel. "
                "For private channels, do /login. Send /help to know more."
            ),
            reply_markup=keyboard
        )
        return  

    # Handle /start with parameters (Token Verification)
    param = message.command[1] if len(message.command) > 1 else None
    freecheck = await chk_user(message, user_id)
    
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return

    if param:
        if user_id in Param and Param[user_id] == param:
            await token.insert_one({
                "user_id": user_id,
                "param": param,
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(hours=3),
            })
            del Param[user_id]   
            await message.reply("✅ You have been verified successfully! Enjoy your session for next 3 hours.")
            return
        else:
            await message.reply("❌ Invalid or expired verification link. Please generate a new token.")
            return

@app.on_message(filters.command("token"))
async def smart_handler(client, message):
    """Handle the /token command generation."""
    user_id = message.chat.id
    
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a premium user no need of token 😉")
        return

    if await is_user_verified(user_id):
        await message.reply("✅ Your free session is already active enjoy!")
    else:
        param = await generate_random_param()
        Param[user_id] = param   

        deep_link = f"https://t.me/{client.me.username}?start={param}"

        shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ Failed to generate the token link. Please try again.")
            return

        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Verify the token now...", url=shortened_url)]]
        )
        
        await message.reply(
            "Click the button below to verify your free access token: \n\n"
            "> What will you get ? \n"
            "1. No time bound upto 3 hours \n"
            "2. Batch command limit will be FreeLimit + 20 \n"
            "3. All functions unlocked", 
            reply_markup=button
        )

