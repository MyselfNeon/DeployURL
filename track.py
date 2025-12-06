# ------------------------------------------------
# File Name: MyselfNeon/track.py
# Description: Headers now managed by main.py Session.
# ------------------------------------------------

import asyncio
import logging
from bs4 import BeautifulSoup
from config import OWNER_ID 
from MyselfNeon.db import db

logger = logging.getLogger(__name__)

async def get_soup(url, client):
    try:
        # Headers are managed by the AsyncSession in main.py
        # This ensures Client Hints match the browser version perfectly.
        response = await client.get(url, allow_redirects=True)
        response.raise_for_status()
        return await asyncio.to_thread(BeautifulSoup, response.content, 'html.parser')
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None

async def broadcast_message(bot, text, disable_preview=False):
    auth_users = await db.get_all_auth_users()
    recipients = set(auth_users)
    recipients.add(OWNER_ID)

    sent_messages = []
    for user_id in recipients:
        try:
            msg = await bot.send_message(user_id, text, disable_web_page_preview=disable_preview)
            sent_messages.append(msg)
            await asyncio.sleep(0.2) 
        except Exception as e:
            logger.error(f"Failed to send alert to {user_id}: {e}")
    return sent_messages

async def check_user_status(http_client, bot):
    # Fetch targets from DB
    targets = await db.get_targets("user")
    current_status_report = {} 

    for target in targets:
        name = target['_id']
        url = target['url']
        
        soup = await get_soup(url, http_client)
        if not soup:
            current_status_report[name] = {"status": "Error", "last_seen": "Connection Failed"}
            continue

        is_online = False
        last_seen_text = "Hidden / Unknown"

        # Parsing Logic
        pairs = soup.select("dl.pairs.pairs--inline")
        for pair in pairs:
            dt = pair.find("dt")
            if dt and "Last seen" in dt.get_text():
                dd = pair.find("dd")
                if dd:
                    last_seen_text = dd.get_text(strip=True)
                    break
        
        lower_text = last_seen_text.lower()
        active_keywords = ["moment ago", "minute ago", "viewing", "posting", "replying", "managing"]
        
        if any(key in lower_text for key in active_keywords):
            is_online = True
        elif soup.find(string="Online now"):
            is_online = True
            last_seen_text = "Online Now"

        # --- LOG ACTIVITY ---
        if is_online:
            await db.log_activity(name)
        # --------------------

        # Alert Logic
        state_key = f"user_status_{name}"
        was_online = await db.get_state(state_key)
        
        if was_online is None:
            await db.set_state(state_key, is_online)
            was_online = is_online

        if is_online and not was_online:
            msg = f"🚨 **__USER ALERT__**\n\n👤 **__{name}** is now **ONLINE__** 🟢\n👀 **__Activity:__** __{last_seen_text}__\n🔗 **__[Profile Link]({url})__**"
            sent_msgs = await broadcast_message(bot, msg, disable_preview=True)
            await db.set_state(state_key, True)
            asyncio.create_task(delete_later(sent_msgs))
        
        elif not is_online and was_online:
            msg = f"💤 **__STATUS UPDATE__**\n\n👤 **__{name}** is now **OFFLINE__** 🔴"
            sent_msgs = await broadcast_message(bot, msg, disable_preview=True)
            await db.set_state(state_key, False)
            asyncio.create_task(delete_later(sent_msgs))
        
        current_status_report[name] = {"status": "Online" if is_online else "Offline", "last_seen": last_seen_text}
        
    return current_status_report

async def check_forums(http_client, bot):
    targets = await db.get_targets("forum")
    forum_counts = {}
    
    for target in targets:
        forum_name = target['_id']
        url = target['url']

        soup = await get_soup(url, http_client)
        if not soup:
            forum_counts[forum_name] = "Error"
            continue

        thread_links = soup.select('.structItem-title a')
        current_threads = []
        for link in thread_links:
            text = link.get_text(strip=True)
            href = link.get('href')
            if href and "threads/" in href:
                full_url = f"https://platinmods.com{href}" if href.startswith('/') else href
                current_threads.append({"title": text, "url": full_url})
        
        forum_counts[forum_name] = len(current_threads)

        state_key = f"forum_threads_{forum_name}"
        previous_threads_list = await db.get_state(state_key) or []
            
        prev_urls = {t['url'] for t in previous_threads_list}
        curr_urls = {t['url'] for t in current_threads}

        new_urls = curr_urls - prev_urls
        removed_urls = prev_urls - curr_urls

        if new_urls:
            for item in current_threads:
                if item['url'] in new_urls:
                    msg = f"🚨 **__NEW THREAD** \n– in {forum_name}__\n\n📝 __{item['title']}\n🔗 **[View Thread]({item['url']})__**"
                    await broadcast_message(bot, msg)

        if removed_urls:
            for item in previous_threads_list:
                if item['url'] in removed_urls:
                    msg = f"🛃 **__THREAD REMOVED** \n– from {forum_name}__\n\n📝 __{item['title']}__"
                    await broadcast_message(bot, msg)

        await db.set_state(state_key, current_threads)

    return forum_counts

async def delete_later(message_list):
    await asyncio.sleep(300)
    for msg in message_list:
        try: await msg.delete()
        except: pass
