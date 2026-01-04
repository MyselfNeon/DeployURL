# ---------------------------------------------------
# File Name: Plans.py
# Author: MyselfNeon
# Original Repo: https://github.com/MyselfNeon/SaveRestrictions-V2
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# ---------------------------------------------------

import asyncio
import datetime
from datetime import timedelta
import pytz

from pyrogram import filters
from MyselfNeon import app
from config import OWNER_ID
from MyselfNeon.core.func import get_seconds
from MyselfNeon.core.mongo import plans_db

# --- Constants ---
IST = pytz.timezone("Asia/Kolkata")

# --- Helper Functions ---
def get_ist_time():
    """Returns current time in IST."""
    return datetime.datetime.now(IST)

def format_expiry_date(date_obj):
    """Formats expiry date to IST string."""
    return date_obj.astimezone(IST).strftime("%d-%m-%Y\n⏱️ Expiry Time : %I:%M:%S %p")

def calculate_time_left(expiry_date):
    """Calculates time remaining string."""
    current_time = get_ist_time()
    # Ensure expiry_date is timezone aware for subtraction
    if expiry_date.tzinfo is None:
        expiry_date = expiry_date.replace(tzinfo=IST)
    else:
        expiry_date = expiry_date.astimezone(IST)
        
    time_left = expiry_date - current_time
    
    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{days} Days, {hours} Hours, {minutes} Minutes"

# --- Bot Commands ---
@app.on_message(filters.command("rem") & filters.user(OWNER_ID))
async def remove_premium(client, message):
    if len(message.command) != 2:
        await message.reply_text("**__Usage :** /rem user_id __")
        return

    user_id = int(message.command[1])
    user = await client.get_users(user_id)
    data = await plans_db.check_premium(user_id)

    if data and data.get("_id"):
        await plans_db.remove_premium(user_id)
        await message.reply_text("__User Removed Successfully__")
        await client.send_message(
            chat_id=user_id,
            text=(
                f"**__Hey {user.mention},__**\n\n"
                f"__Your **Premium** access has been removed.__\n"
                f"**__Thank You** for using our service__."
            )
        )
    else:
        await message.reply_text("🚫 __Unable to remove user__\nᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ, ɪᴛ ᴡᴀꜱ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ɪᴅ ?")

@app.on_message(filters.command("myplan"))
async def myplan(client, message):
    user_id = message.from_user.id
    user_mention = message.from_user.mention
    data = await plans_db.check_premium(user_id)

    if data and data.get("expire_date"):
        expiry = data.get("expire_date")
        expiry_str = format_expiry_date(expiry)
        time_left_str = calculate_time_left(expiry)

        await message.reply_text(
            f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n"
            f"👤 ᴜꜱᴇʀ : {user_mention}\n"
            f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
            f"⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n"
            f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str}"
        )
    else:
        await message.reply_text(f"ʜᴇʏ {user_mention},\n\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs")

@app.on_message(filters.command("check") & filters.user(OWNER_ID))
async def get_premium(client, message):
    if len(message.command) != 2:
        await message.reply_text("ᴜꜱᴀɢᴇ : /check user_id")
        return

    user_id = int(message.command[1])
    user = await client.get_users(user_id)
    data = await plans_db.check_premium(user_id)

    if data and data.get("expire_date"):
        expiry = data.get("expire_date")
        expiry_str = format_expiry_date(expiry)
        time_left_str = calculate_time_left(expiry)
        
        expiry_ist = expiry.astimezone(IST)
        current_time = get_ist_time()
        time_left = expiry_ist - current_time
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        english_time_left = f"{days} days, {hours} hours, {minutes} minutes"

        await message.reply_text(
            f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n"
            f"👤 ᴜꜱᴇʀ : {user.mention}\n"
            f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
            f"⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {english_time_left}\n"
            f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str}"
        )
    else:
        await message.reply_text("ɴᴏ ᴀɴʏ ᴘʀᴇᴍɪᴜᴍ ᴅᴀᴛᴀ ᴏꜰ ᴛʜᴇ ᴡᴀꜱ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ !")

@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def give_premium_cmd_handler(client, message):
    if len(message.command) != 4:
        await message.reply_text("Usage : /add user_id time (e.g., '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year')")
        return

    joining_time = get_ist_time().strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p")
    user_id = int(message.command[1])
    user = await client.get_users(user_id)
    duration_str = message.command[2] + " " + message.command[3]
    
    seconds = await get_seconds(duration_str)

    if seconds > 0:
        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        await plans_db.add_premium(user_id, expiry_time)
        
        data = await plans_db.check_premium(user_id)
        expiry = data.get("expire_date")
        expiry_str = format_expiry_date(expiry)

        # Admin confirmation
        await message.reply_text(
            f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅\n\n"
            f"👤 ᴜꜱᴇʀ : {user.mention}\n"
            f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
            f"⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{duration_str}</code>\n\n"
            f"⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {joining_time}\n\n"
            f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str} \n\n"
            f"__**Powered by Team SPY__**",
            disable_web_page_preview=True
        )

        # User notification
        await client.send_message(
            chat_id=user_id,
            text=(
                f"👋 ʜᴇʏ {user.mention},\n"
                f"ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴘᴜʀᴄʜᴀꜱɪɴɢ ᴘʀᴇᴍɪᴜᴍ.\n"
                f"ᴇɴᴊᴏʏ !! ✨🎉\n\n"
                f"⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{duration_str}</code>\n"
                f"⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {joining_time}\n\n"
                f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str}"
            ),
            disable_web_page_preview=True
        )
    else:
        await message.reply_text("Invalid time format. Please use '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year'")

@app.on_message(filters.command("transfer"))
async def transfer_premium(client, message):
    if len(message.command) != 2:
        await message.reply_text("⚠️ **Usage:** /transfer user_id\n\nReplace `user_id` with the new user's ID.")
        return

    new_user_id = int(message.command[1])
    sender_user_id = message.from_user.id
    
    sender_user = await client.get_users(sender_user_id)
    new_user = await client.get_users(new_user_id)

    # Fetch sender's premium plan details
    data = await plans_db.check_premium(sender_user_id)

    if data and data.get("_id"):
        expiry = data.get("expire_date")

        # Remove from sender, Add to new user
        await plans_db.remove_premium(sender_user_id)
        await plans_db.add_premium(new_user_id, expiry)

        # Formatting
        expiry_str = expiry.astimezone(IST).strftime("%d-%m-%Y\n⏱️ **Expiry Time:** %I:%M:%S %p")
        transfer_time = get_ist_time().strftime("%d-%m-%Y\n⏱️ **Transfer Time:** %I:%M:%S %p")

        # Confirmation to sender
        await message.reply_text(
            f"✅ **Premium Plan Transferred Successfully!**\n\n"
            f"👤 **From:** {sender_user.mention}\n"
            f"👤 **To:** {new_user.mention}\n"
            f"⏳ **Expiry Date:** {expiry_str}\n\n"
            f"__Powered by Team SPY__ 🚀"
        )

        # Notification to new user
        await client.send_message(
            chat_id=new_user_id,
            text=(
                f"👋 **Hey {new_user.mention},**\n\n"
                f"🎉 **Your Premium Plan has been Transferred!**\n"
                f"🛡️ **Transferred From:** {sender_user.mention}\n\n"
                f"⏳ **Expiry Date:** {expiry_str}\n"
                f"📅 **Transferred On:** {transfer_time}\n\n"
                f"__Enjoy the Service!__ ✨"
            )
        )
    else:
        await message.reply_text("⚠️ **You are not a Premium user!**\n\nOnly Premium users can transfer their plans.")

async def premium_remover():
    all_users = await plans_db.premium_users()
    removed_users = []
    not_removed_users = []

    for user_id in all_users:
        try:
            user = await app.get_users(user_id)
            chk_time = await plans_db.check_premium(user_id)

            if chk_time and chk_time.get("expire_date"):
                expiry_date = chk_time["expire_date"]
                name = user.first_name

                if expiry_date <= datetime.datetime.now():
                    await plans_db.remove_premium(user_id)
                    await app.send_message(user_id, text=f"Hello {name}, your premium subscription has expired.")
                    print(f"{name}, your premium subscription has expired.")
                    removed_users.append(f"{name} ({user_id})")
                else:
                    current_time = datetime.datetime.now()
                    time_left = expiry_date - current_time

                    days = time_left.days
                    hours, remainder = divmod(time_left.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    if days > 0:
                        remaining_time = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
                    elif hours > 0:
                        remaining_time = f"{hours} hours, {minutes} minutes, {seconds} seconds"
                    elif minutes > 0:
                        remaining_time = f"{minutes} minutes, {seconds} seconds"
                    else:
                        remaining_time = f"{seconds} seconds"

                    print(f"{name} : Remaining Time : {remaining_time}")
                    not_removed_users.append(f"{name} ({user_id})")
        except Exception as e:
            # Catching Exception is safer than bare except, but logic is preserved
            await plans_db.remove_premium(user_id)
            print(f"Unknown users captured : {user_id} removed. Error: {e}")
            removed_users.append(f"Unknown ({user_id})")

    return removed_users, not_removed_users

@app.on_message(filters.command("freez") & filters.user(OWNER_ID))
async def refresh_users(_, message):
    removed_users, not_removed_users = await premium_remover()
    
    removed_text = "\n".join(removed_users) if removed_users else "No users removed."
    not_removed_text = "\n".join(not_removed_users) if not_removed_users else "No users remaining with premium."
    
    summary = (
        f"**Here is the Summary...**\n\n"
        f"> **Removed Users:**\n{removed_text}\n\n"
        f"> **Not Removed Users:**\n{not_removed_text}"
    )
    await message.reply(summary)
