## 🌐 Website Monitor Bot

A fully automated monitoring bot for websites built using **Pyrogram**, **curl_cffi**, **Motor (MongoDB)**, **Flask**, and **asynchronous scraping** via BeautifulSoup.  
Designed for tracking user status, monitoring forum threads, and detecting changes — all with real-time Telegram alerts.

## ✨ Features
- User online/offline tracking  
- New forum thread detection  
- Removed thread detection  
- MongoDB support for persistent targets  
- Add/remove targets dynamically through Telegram  
- Manual `/check` command with summary  
- Background scheduler with randomized intervals  
- Keep-alive support for Render/Railway  
- Chrome-like fetching using curl_cffi  

## 🧩 How It Works
1. Fetches target URLs with curl_cffi (Chrome impersonation)  
2. Parses data using BeautifulSoup  
3. Compares scraped data with MongoDB entries  
4. Detects status changes & new/removed threads  
5. Sends Telegram alerts to authorized users  
6. Runs continuously using async scheduler + Flask keep-alive  

## 🚀 Installation
```bash
git clone https://github.com/MyselfNeon/Website-Monitor-neon
cd Website-Monitor-neon
pip install -r requirements.txt
```

## ⚙️ Configuration
Create a `.env` file or set these environment variables:

```
API_ID = 12345
API_HASH = "your_telegram_hash"
BOT_TOKEN = "your_bot_token"

OWNER_ID = 123456789
DB_URI = "mongodb+srv://..."
DB_NAME = "PMT-Testing"

# Optional
MIN_CHECK_INTERVAL = 8
MAX_CHECK_INTERVAL = 12
PORT = 8080
```

## ▶️ Running the Bot
```bash
python main.py
```

## 🧪 Commands

### General
- `/start` — Check bot status & get your ID  
- `/check` — Manually run a check + get summary  

### Admin / Management
- `/add_user <Name> <URL>` — Add a user to monitor  
- `/del_user <Name>` — Remove a tracked user  
- `/add_forum <Name> <URL>` — Add a forum section  
- `/del_forum <Name>` — Remove a forum section  
- `/list` — Show all tracked users/forums & authorized users  
- `/auth <ID>` — Authorize a user to receive alerts  
- `/unauth <ID>` — Revoke authorization  
- `/restart` — Restart the bot (Owner only)  

## 🌐 Deployment (Render / Railway / Replit)
1. Set the `KEEP_ALIVE_URL` inside `main.py`  
2. Add environment variables to the platform  
3. Deploy normally  
4. Bot stays awake using the Flask background task  

## ❤️ Author
**Neon** — https://github.com/MyselfNeon
