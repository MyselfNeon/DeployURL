# ------------------------------------------------
# File Name: MyselfNeon/useless.py
# Description: Handles System & Management Commands
# ------------------------------------------------

import os
import sys
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from MyselfNeon.db import db
from config import OWNER_IDS 

logger = logging.getLogger(__name__)

# Key to store restart message ID so we can delete it after reboot
RESTART_MSG_KEY = "restart_message_info"

# Helper: Strict Owner Check
async def is_owner(message: Message):
    if not message.from_user: return False
    if message.from_user.id in OWNER_IDS: return True
    
    # Access Denied Animation
    try:
        m = await message.reply_sticker("CAACAgIAAxkBAAJF4WkjF7pMqaiigSJbxdN2p5iDrzjFAAJ-GgACglXYSXgCrotQHjibHgQ")
        await asyncio.sleep(1)
        await m.delete()
    except: pass
    
    await message.reply("⛔ **__ACCESS DENIED__** ⛔\n\n__Only the Bot Owner can use this command.__")
    return False

def register_useless_commands(bot: Client):
    """
    Registers system and management commands.
    """

    # --- RESTART COMMAND ---
    @bot.on_message(filters.command("restart"))
    async def restart_cmd(client: Client, message: Message):
        if not await is_owner(message): return

        restart_message = await message.reply_text("🔄 **__Restarting Bot...__**\n\n__Reloading scripts and reconnecting...__")
        try:
            logger.info(f"Owner {message.from_user.id} triggered bot restart.")
            await db.set_state(RESTART_MSG_KEY, {
                "chat_id": restart_message.chat.id,
                "message_id": restart_message.id,
            })
            await asyncio.sleep(1)
            os.execlp(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            logger.error(f"Failed to execute restart: {e}")
            await restart_message.edit_text(f"❌ **__Restart Failed: {e}__**")

    # --- ADD USER TARGET ---
    @bot.on_message(filters.command("add_user"))
    async def add_user_target(client: Client, message: Message):
        if not await is_owner(message): return
        args = message.command
        
        if len(args) < 3: 
            return await message.reply("⚠️ Usage: /add_user <Name> <URL>")
            
        url = args[-1]
        name = " ".join(args[1:-1])
        await db.add_target("user", name, url, "span.userTitle")
        await message.reply(f"✅ **Tracking Added:** {name}")

    # --- DELETE USER TARGET ---
    @bot.on_message(filters.command("del_user"))
    async def del_user_target(client: Client, message: Message):
        if not await is_owner(message): return
        
        if len(message.command) < 2: 
            return await message.reply("⚠️ Usage: /del_user <Name>")
            
        name = " ".join(message.command[1:])
        if await db.remove_target(name): await message.reply(f"🗑 **Deleted User Target:** {name}")
        else: await message.reply(f"❌ Could not find user: {name}")

    # --- ADD FORUM TARGET ---
    @bot.on_message(filters.command("add_forum"))
    async def add_forum_target(client: Client, message: Message):
        if not await is_owner(message): return
        args = message.command
        
        if len(args) < 3: 
            return await message.reply("⚠️ Usage: /add_forum <Name> <URL>")
            
        url = args[-1]
        name = " ".join(args[1:-1])
        await db.add_target("forum", name, url)
        await message.reply(f"✅ **Forum Added:** {name}")

    # --- DELETE FORUM TARGET ---
    @bot.on_message(filters.command("del_forum"))
    async def del_forum_target(client: Client, message: Message):
        if not await is_owner(message): return
        
        if len(message.command) < 2: 
            return await message.reply("⚠️ Usage: /del_forum <Name>")
            
        name = " ".join(message.command[1:])
        if await db.remove_target(name): await message.reply(f"🗑 **Deleted Forum Target:** {name}")
        else: await message.reply(f"❌ Could not find forum: {name}")

    # --- AUTHORIZE USER ---
    @bot.on_message(filters.command("auth"))
    async def auth_user_cmd(client: Client, message: Message):
        if not await is_owner(message): return
        
        if len(message.command) < 2: 
            return await message.reply("⚠️ Usage: /auth <User ID>")
            
        try:
            uid = int(message.command[1])
            await db.add_auth_user(uid)
            await message.reply(f"🔓 **User {uid} Authorized.**")
        except ValueError: await message.reply("❌ User ID must be a number.")

    # --- UNAUTHORIZE USER ---
    @bot.on_message(filters.command("unauth"))
    async def unauth_user_cmd(client: Client, message: Message):
        if not await is_owner(message): return
        
        if len(message.command) < 2: 
            return await message.reply("⚠️ Usage: /unauth <User ID>")
            
        try:
            uid = int(message.command[1])
            await db.remove_auth_user(uid)
            await message.reply(f"🔒 **User {uid} Removed.**")
        except ValueError: await message.reply("❌ User ID must be a number.")

    # --- LIST CONFIGURATION ---
    @bot.on_message(filters.command("list"))
    async def list_targets(client: Client, message: Message):
        if not await is_owner(message): return
        users = await db.get_targets("user")
        forums = await db.get_targets("forum")
        auths = await db.get_all_auth_users()
        msg = "**📊 __Current Configuration__**\n\n**👤 Users to Track:**\n"
        for u in users: msg += f"- {u['_id']}\n"
        msg += "\n**📚 Forums to Track:**\n"
        for f in forums: msg += f"- {f['_id']}\n"
        msg += "\n**🔓 Authorized IDs:**\n"
        for a in auths: msg += f"- `{a}`\n"
        await message.reply(msg)

    # --- ACTIVITY GRAPH ---
    @bot.on_message(filters.command("activity"))
    async def activity_cmd(client: Client, message: Message):
        if not await is_owner(message): return

        if len(message.command) < 2:
            return await message.reply("⚠️ Usage: /activity <User Name>")
        
        target_name = " ".join(message.command[1:])
        
        tmp = await message.reply_sticker("CAACAgEAAxkBAAJHQWkqZs4YE4Oxlil7LNLgruuoGkkaAAItAgACpyMhRD1AMMntg7S2HgQ")
        
        logs = await db.get_activity_data(target_name)
        
        if not logs:
            await tmp.delete()
            return await message.reply(f"📉 **__No activity data found for: {target_name}__**\n__Wait for them to come online so I can start logging!__")

        hours = {i: 0 for i in range(24)}
        for timestamp in logs:
            hours[timestamp.hour] += 1

        max_val = max(hours.values()) if hours.values() else 1
        graph_lines = []
        
        graph_lines.append(f"📊 **__Activity Graph: {target_name}__**\n")
        graph_lines.append("`Hour  Activity Lvl`")
        
        BAR_CHAR = "■"
        
        for h in range(24):
            count = hours[h]
            if count == 0: continue 
            bar_len = int((count / max_val) * 10)
            bar_len = max(1, bar_len)
            time_str = f"{h:02d}:00"
            bar_str = BAR_CHAR * bar_len
            graph_lines.append(f"`{time_str} {bar_str}`")

        if len(graph_lines) == 2:
            graph_lines.append("__Data recorded but spread too thin to graph yet.__")

        await client.send_message(message.chat.id, "\n".join(graph_lines))
        await tmp.delete()

    logger.info("System & Management commands registered.")
