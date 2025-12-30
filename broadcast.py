# ---------------------------------------------------
# File Name: Telegraph.py
# Author: MyselfNeon
# Original Repo: https://github.com/MyselfNeon/SaveRestrictions-V2
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# ---------------------------------------------------

import os
import re
import time
import logging
import requests
from telegraph import Telegraph
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from MyselfNeon import app 

# Logger setup
logger = logging.getLogger(__name__)

# --- Configuration ---
DOMAIN = "graph.org"
CATBOX_API_URL = "https://catbox.moe/user/api.php"
IMGBB_API_URL = "https://api.imgbb.com/1/upload"

EMOJI_PATTERN = re.compile(r'<emoji id="\d+">')
TITLE_PATTERN = re.compile(r"title:? (.*)", re.IGNORECASE)

# --- State ---
user_sessions = {} 
edit_sessions = {} 
last_update_time = {}

# --- Filters ---
async def check_session_func(_, __, message):
    return message.from_user and message.from_user.id in user_sessions

async def check_edit_func(_, __, message):
    return message.from_user and message.from_user.id in edit_sessions

has_active_session = filters.create(check_session_func)
has_edit_session = filters.create(check_edit_func)

# --- Helpers ---
async def simple_progress(current, total, message):
    percentage = current * 100 / total
    now = time.time()
    last_time = last_update_time.get(message.id, 0)
    if now - last_time > 3 or current == total:
        last_update_time[message.id] = now
        try:
            await message.edit(f"⏳ **__Downloading ... {int(percentage)}%__**")
        except Exception:
            pass

def upload_file(file_path, expiration=None):
    imgbb_key = os.getenv("IMGBB_API_KEY")
    if imgbb_key:
        try:
            params = {"key": imgbb_key}
            if expiration: params["expiration"] = expiration
            with open(file_path, "rb") as f:
                response = requests.post(IMGBB_API_URL, params=params, files={"image": f}, timeout=60)
            if response.ok:
                data = response.json()["data"]
                return {"provider": "ImgBB", "url": data["url"], "delete_url": data.get("delete_url")}
        except Exception as e:
            logger.error(f"ImgBB Error: {e}")

    try:
        with open(file_path, "rb") as f:
            response = requests.post(CATBOX_API_URL, data={"reqtype": "fileupload", "userhash": ""}, files={"fileToUpload": f}, timeout=60)
        if response.ok:
            return {"provider": "Catbox", "url": response.text.strip(), "delete_url": None}
    except Exception as e:
        logger.error(f"Catbox Error: {e}")
    return None

def get_telegraph_client():
    token = os.getenv("TELEGRAPH_TOKEN")
    if token:
        return Telegraph(domain=DOMAIN, access_token=token), True
    else:
        t = Telegraph(domain=DOMAIN)
        t.create_account(short_name="MyselfNeon")
        return t, False

# --- Handler 1: /graph (Upload Mode) ---
@app.on_message(filters.command("graph") & filters.private)
async def graph_command_handler(client, message: Message):
    user_id = message.from_user.id
    user_sessions.pop(user_id, None)
    edit_sessions.pop(user_id, None)

    mode_text = "**__Permanent Mode__** ♾️"
    expiration = 0

    if len(message.command) > 1:
        arg = message.command[1].lower()
        
        # EDIT MODE CHECK
        if "graph.org" in arg or "telegra.ph" in arg:
            if not os.getenv("TELEGRAPH_TOKEN"):
                await message.reply_text("**__⚠️ Error:** `TELEGRAPH_TOKEN` missing.__")
                return

            path = arg.split("/")[-1]
            edit_sessions[user_id] = path
            
            await message.reply_text(
                f"**__📝 Edit Mode Activated__**\n\n"
                f"**__Editing Post:** {path}__\n"
                "**__Send New Text to Update.__**",
                quote=True
            )
            return

        # TIMER CHECK
        elif "m" in arg: expiration = int(arg.replace("m", "")) * 60
        elif "h" in arg: expiration = int(arg.replace("h", "")) * 3600
        elif arg.isdigit(): expiration = int(arg)
        
        if expiration > 0:
            mode_text = f"🚮 Auto-Delete Mode \n⏰ ({int(expiration/60)} mins)"

    user_sessions[user_id] = expiration
    await message.reply_text(
        f"**__✅ Mode Initiated !__**\n**__Mode: {mode_text}__**\n\n"
        "**__Please Send the Photo or Text__**",
        quote=True
    )

# --- Handler 2: Photo Upload ---
@app.on_message(filters.photo & filters.private & has_active_session)
async def photo_handler(client, message: Message):
    expiration = user_sessions.pop(message.from_user.id, 0)
    msg = await message.reply_text("🚨 **__Processing Photo ... 0%__**", quote=True)
    
    file = None
    location = f"./downloads/{message.from_user.id}_{int(time.time())}/"

    try:
        file = await message.download(location, progress=simple_progress, progress_args=(msg,))
        await msg.edit("**__☁️ Uploading Now ...__**")
        
        media_data = upload_file(file, expiration=expiration)
        if not media_data:
            await msg.edit("**__❌ Upload Failed.__**")
            return

        buttons = [[InlineKeyboardButton("🌐 Vɪᴇᴡ Iᴍᴀɢᴇ", url=media_data["url"])]]
        if media_data.get("delete_url") and expiration == 0:
            buttons.append([InlineKeyboardButton("🗑️ Dᴇʟᴇᴛᴇ (Wᴇʙ)", url=media_data["delete_url"])])

        info_text = f"✅ **__Upload Successful !__**\n🔗 **__[Click Here to View]({media_data['url']})__**\n📡 **__Provider: {media_data['provider']}__**"
        if expiration > 0: info_text += f"\n🕓 **__Auto-Deletes in: {int(expiration/60)} mins__**"

        await msg.edit(info_text, reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as e:
        await msg.edit(f"**__Error:** {e}__")
    finally:
        last_update_time.pop(msg.id, None)
        if file and os.path.exists(file): os.remove(file)
        if os.path.exists(location): os.rmdir(location)

# --- Handler 3: Create Text Post ---
@app.on_message(filters.text & filters.private & has_active_session)
async def text_handler(client, message: Message):
    user_sessions.pop(message.from_user.id, None)
    msg = await message.reply_text("**__Processing Text ...😇__**", quote=True)

    telegraph, is_auth = get_telegraph_client()

    try:
        content = message.text.html
        content = re.sub(EMOJI_PATTERN, "", content).replace("</emoji>", "")

        title_match = re.findall(TITLE_PATTERN, content)
        if title_match:
            title = title_match[0]
            content = "\n".join(content.splitlines()[1:])
        else:
            title = message.from_user.first_name

        content = content.replace("\n", "<br>")
        
        response = telegraph.create_page(
            title=title,
            html_content=content,
            author_name=str(message.from_user.first_name),
            author_url=f"https://t.me/{message.from_user.username}" if message.from_user.username else None
        )
        
        page_path = response['path']
        page_url = f"https://{DOMAIN}/{page_path}"

        buttons = []
        if is_auth:
            buttons = [
                [
                    InlineKeyboardButton("📝 Edit Post", callback_data=f"edit_start_{page_path}"),
                    InlineKeyboardButton("🗑️ Delete Post", callback_data=f"delete_post_{page_path}")
                ]
            ]
        
        await msg.edit(f"**__✅ Generated Post Link:__**\n**__{page_url}__**", reply_markup=InlineKeyboardMarkup(buttons) if buttons else None)

    except Exception as e:
        await msg.edit(f"**__Error:** {e}__")

# --- Handler 4: Callback for Edit Button ---
@app.on_callback_query(filters.regex(r"^edit_start_(.*)"))
async def edit_callback_handler(client, query: CallbackQuery):
    path = query.matches[0].group(1)
    edit_sessions[query.from_user.id] = path
    
    await query.message.reply_text(
        f"**__📝 Edit Mode Activated__**\n\n"
        f"**__Editing Post:** {path}__\n"
        "🆕 **__Send new Text to Update.__**"
    )
    await query.answer("Edit Mode Started")

# --- Handler 5: Callback for Delete Button ---
@app.on_callback_query(filters.regex(r"^delete_post_(.*)"))
async def delete_post_callback(client, query: CallbackQuery):
    path = query.matches[0].group(1)
    
    telegraph, is_auth = get_telegraph_client()
    if not is_auth:
        await query.answer("Error: Token missing.", show_alert=True)
        return

    try:
        telegraph.edit_page(
            path=path,
            title="Deleted",
            html_content="<p>Deleted ❌ nothing here</p>",
            author_name="Ghost", 
            return_content=False
        )
        await query.message.edit_text(f"**__🛃 Post Deleted.**\n**__https://{DOMAIN}/{path}"__**)
        await query.answer("Post Wiped Successfully.")
    except Exception as e:
        await query.answer(f"Failed to Delete: {e}", show_alert=True)

# --- Handler 6: Process Edit Text ---
@app.on_message(filters.text & filters.private & has_edit_session)
async def process_edit_handler(client, message: Message):
    # Retrieve & Remove Session (One-time action)
    path = edit_sessions.pop(message.from_user.id) 
    
    msg = await message.reply_text("**__Updating Post...⏳__**", quote=True)

    telegraph, is_auth = get_telegraph_client()
    if not is_auth:
        await msg.edit("**❌ Error:** Token missing.")
        return

    try:
        content = message.text.html
        content = re.sub(EMOJI_PATTERN, "", content).replace("</emoji>", "")

        title_match = re.findall(TITLE_PATTERN, content)
        if title_match:
            title = title_match[0]
            content = "\n".join(content.splitlines()[1:])
        else:
            title = "Updated Post"

        content = content.replace("\n", "<br>")
        
        telegraph.edit_page(
            path=path,
            title=title,
            html_content=content,
            author_name=str(message.from_user.first_name),
            author_url=f"https://t.me/{message.from_user.username}" if message.from_user.username else None
        )
        
        # Same Format As Generation
        buttons = [
            [
                InlineKeyboardButton("📝 Edit Post", callback_data=f"edit_start_{path}"),
                InlineKeyboardButton("🗑️ Delete Post", callback_data=f"delete_post_{path}")
            ]
        ]
        
        await msg.edit(f"**__✅ Post Updated!__**\nhttps://{DOMAIN}/{path}", reply_markup=InlineKeyboardMarkup(buttons))

    except Exception as e:
        await msg.edit(f"**__Update Failed.__**\nError: {e}")
