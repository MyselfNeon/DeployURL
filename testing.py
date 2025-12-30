# ---------------------------------------------------
# File Name: Shrink.py
# Author: MyselfNeon
# Original Repo: https://github.com/MyselfNeon/SaveRestrictions-V2
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# ---------------------------------------------------

import random
import string
import requests
import aiohttp
import asyncio
from pyrogram import enums
from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto

from MyselfNeon import app
from MyselfNeon.core.func import *
from config import MONGO_DB, WEBSITE_URL, AD_API, LOG_GROUP

# --- DATABASE & GLOBALS ---
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]
token = tdb["tokens"]

Param = {}
MEDIA_CACHE = {}

# --- REACTIONS LIST ---
REACTIONS = [
    "🤝", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩",
    "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡",
    "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"
]

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

async def get_cached_file_id(client, chat_id, msg_id):
    """Fetch file_id only if not already in cache to make buttons faster."""
    cache_key = f"{chat_id}_{msg_id}"
    if cache_key in MEDIA_CACHE:
        return MEDIA_CACHE[cache_key]
    try:
        msg = await client.get_messages(chat_id, msg_id)
        if msg.photo:
            file_id = msg.photo.file_id
            MEDIA_CACHE[cache_key] = file_id
            return file_id
    except:
        pass
    return None

# --- COMMAND HANDLERS ---
@app.on_message(filters.command("start"))
async def token_handler(client, message):
    """Handle the /start command."""
    
    # --- 1. Random Reaction Logic ---
    try:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    except Exception:
        pass 

    join = await subscribe(client, message)
    if join == 1:
        return

    chat_id = -1002158258466
    user_id = message.chat.id
    
    if len(message.command) <= 1:
        
        # --- NEW STICKER ANIMATION ---
        try:
            m = await message.reply_sticker("CAACAgIAAxkBAAJQ1GlT1fawhBKM1pfJ2jaULSeEOgIwAAKOFQACJU3BSY8WTX7r0TbzHgQ")
            await asyncio.sleep(1)
            await m.delete()
        except Exception:
            pass
            
        file_id = await get_cached_file_id(client, chat_id, 200)
        
        # --- Mention Automatically ---
        mention = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Mᴏʀᴇ Bᴏᴛs 🤖", callback_data="more_bots"),
                InlineKeyboardButton("Uᴘᴅᴀᴛᴇs 🚨", url="https://t.me/NeonFiles")
            ],   
            [
                InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ 👨‍💻", url="https://t.me/MyselfNeon"),
                InlineKeyboardButton("Aʙᴏᴜᴛ Mᴇ 😎", callback_data="about_btn")
            ]    
        ])
        
        if file_id:
            await message.reply_photo(
                file_id,
                caption=(
                    f"<b><i><blockquote>Yoo {mention} !! Welcome Aboard</blockquote>\n"
                    "<blockquote>I Can Save Posts From Channels or Groups Even When Forwarding is Disabled (Yep, I’m That Powerful 😎)\n\n"
                    "For Public Channel Just Send the Link of the Post & For Private Channel Use /login First 🔑</blockquote></i></b>"
                ),
                parse_mode=enums.ParseMode.HTML,
                reply_markup=keyboard
            )
        else:
            await message.reply("Error: Start image (ID 200) not found in channel.")
        return  

    # --- Handle /start with parameters (Token Verification) ---
    param = message.command[1] if len(message.command) > 1 else None
    freecheck = await chk_user(message, user_id)
    
    if freecheck != 1:
        await message.reply("You are a Premium user no need of Token 😉")
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
            await message.reply("✅ You have been Verified Successfully! Enjoy your Session for next 3 Hours.")
            return
        else:
            await message.reply("❌ Invalid or Expired Verification Link. Please Generate a new Token.")
            return

@app.on_message(filters.command("token"))
async def smart_handler(client, message):
    """Handle the /token command generation."""
    user_id = message.chat.id
    
    freecheck = await chk_user(message, user_id)
    if freecheck != 1:
        await message.reply("You are a Premium User no need of Token 😉")
        return

    if await is_user_verified(user_id):
        await message.reply("✅ Your free Session is Already active Enjoy!")
    else:
        param = await generate_random_param()
        Param[user_id] = param   

        deep_link = f"https://t.me/{client.me.username}?start={param}"

        shortened_url = await get_shortened_url(deep_link)
        if not shortened_url:
            await message.reply("❌ Failed to Generate the Token Link. Please try again.")
            return

        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Verify the Token now...", url=shortened_url)]]
        )
        
        await message.reply(
            "🚨 **__Click the Button Below to Verify your Free Access Token:__** \n\n"
            "> **What will you get ?** \n"
            "**__1. No Time Bound upto 3 Hours__** \n"
            "**__2. Removed Batch Command Limit \n"
            "**__3. FreeLimit + 20 \n"
            "**__4. More Functions Unlocked__**", 
            reply_markup=button
    )

# --- CALLBACK HANDLERS ---
@app.on_callback_query(filters.regex("about_btn"))
async def about_page(client, cb: CallbackQuery):
    await cb.answer()
    
    bot = await client.get_me()
    me = f"<a href='tg://user?id={bot.id}'>{bot.first_name}</a>"

    about_text = f"""<b><blockquote>‣ ⁉️ 𝐌𝐘 𝐃𝐄𝐓𝐀𝐈𝐋𝐒</blockquote>
<blockquote><i>• Mʏ Nᴀᴍᴇ : {me}
• Mʏ Bᴇsᴛ Fʀɪᴇɴᴅ : <a href='tg://settings'>Tʜɪs Sᴡᴇᴇᴛɪᴇ ❤️</a> 
• Dᴇᴠᴇʟᴏᴘᴇʀ : <a href='https://t.me/MyselfNeon'>@MʏsᴇʟғNᴇᴏɴ</a> 
• Lɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ</a> 
• Lᴀɴɢᴜᴀɢᴇ : <a href='https://www.python.org/download/releases/3.0/'>Pʏᴛʜᴏɴ 𝟹</a> 
• DᴀᴛᴀBᴀsᴇ : <a href='https://www.mongodb.com/'>Mᴏɴɢᴏ DB</a> 
• Bᴏᴛ Sᴇʀᴠᴇʀ : <a href='https://heroku.com'>Hᴇʀᴏᴋᴜ</a> 
• Bᴜɪʟᴅ Sᴛᴀᴛᴜs : ᴠ𝟸.𝟽.𝟷 [Sᴛᴀʙʟᴇ]</i></blockquote></b>"""

    about_buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ 🔊", url="https://t.me/+o1s-8MppL2syYTI9"),
                InlineKeyboardButton("Sᴏᴜʀᴄᴇ Cᴏᴅᴇ 🆘", url="https://myselfneon.github.io/neon/")
            ],
            [
                InlineKeyboardButton("Cʟᴏsᴇ ❌", callback_data="close"),
                InlineKeyboardButton("⬅️ Bᴀᴄᴋ", callback_data="back_to_start")
            ]
        ]
    )
    
    # Image URL for About Page
    IMAGE_URL = "https://files.catbox.moe/w36xox.jpg"

    await cb.message.edit_media(
        media=InputMediaPhoto(
            media=IMAGE_URL,
            caption=about_text,
            parse_mode=enums.ParseMode.HTML
        ),
        reply_markup=about_buttons
    )

@app.on_callback_query(filters.regex("more_bots"))
async def more_bots_page(client, cb: CallbackQuery):
    await cb.answer()
    
    text = (
        "<b>🤖 My Other Bots:</b>\n\n"
        "• @Bot1\n"
        "• @bot2"
    )
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Cʟᴏsᴇ ❌", callback_data="close"),
            InlineKeyboardButton("⬅️ Bᴀᴄᴋ", callback_data="back_to_start")
        ]
    ])
    
    # Image URL for More Bots
    IMAGE_URL = "https://files.catbox.moe/7c5u70.jpg"

    await cb.message.edit_media(
        media=InputMediaPhoto(
            media=IMAGE_URL,
            caption=text,
            parse_mode=enums.ParseMode.HTML
        ),
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("close"))
async def close_msg(client, cb: CallbackQuery):
    await cb.message.delete()

@app.on_callback_query(filters.regex("back_to_start"))
async def back_to_start(client, cb: CallbackQuery):
    await cb.answer()
    
    chat_id = -1002158258466
    
    # Fetch Start Image (ID 200) from Cache
    file_id = await get_cached_file_id(client, chat_id, 200)
    
    mention = f"<a href='tg://user?id={cb.from_user.id}'>{cb.from_user.first_name}</a>"
    
    caption = (
        f"<b><i><blockquote>Yoo {mention} !! Welcome Aboard</blockquote>\n"
        "<blockquote>I Can Save Posts From Channels or Groups Even When Forwarding is Disabled (Yep, I’m That Powerful 😎)\n\n"
        "For Public Channel Just Send the Link of the Post & For Private Channel Use /login First 🔑</blockquote></i></b>"
    )
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Mᴏʀᴇ Bᴏᴛs 🤖", callback_data="more_bots"),
            InlineKeyboardButton("Uᴘᴅᴀᴛᴇs 🚨", url="https://t.me/NeonFiles")
        ],   
        [
            InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ 👨‍💻", url="https://t.me/MyselfNeon"),
            InlineKeyboardButton("Aʙᴏᴜᴛ Mᴇ 😎", callback_data="about_btn")
        ]    
    ])
    
    if file_id:
        await cb.message.edit_media(
            media=InputMediaPhoto(
                media=file_id, 
                caption=caption,
                parse_mode=enums.ParseMode.HTML
            ),
            reply_markup=keyboard
        )
    else:
        await cb.answer("Error: Start image (ID 200) not found!", show_alert=True)
      
# --- MyselfNeon 🎉 ---
# --- Telegram/Github = @MyselfNeon ---
