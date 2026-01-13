## *Website Monitor Bot* 🌐

*A fully automated, stealthy monitoring bot for Websites built using Pyrogram curl_cffi (Browser Impersonation), MongoDB (Motor), Flask, and asynchronous scraping with BeautifulSoup.*

---

### ✨ *Features*

- *User Online/Offline tracking*
- *New forum thread detection & removed thread alerts*
- *Advanced Anti-Detection (Browser Impersonation & Random Delays)*
- *Auto-Healing for Errors*
- *Full Admin Management via Telegram (Add/Remove targets dynamically)*
- *MongoDB Database support for persistent state tracking*
- *Manual `/check` command with instant snapshot reporting*
- *Flask Web Server with custom Neon HTML Health Check*

---

### 📂 *Project Structure*

- **`main.py`**: *The core entry point. Handles the scheduler, self-healing logic, and bot startup.*
- **`config.py`**: *Manages environment variables and configuration settings.*
- **`app.py`**: *Flask web server providing a styled health-check page.*
- **`MyselfNeon/db.py`**: *Async MongoDB handler. Manages states, targets, auth, and logs.*
- **`MyselfNeon/track.py`**: *Contains the scraping logic (`curl_cffi`) and status detection algorithms.*
- **`MyselfNeon/useless.py`**: *Handles system & management commands (Restart, Auth, Add/Del Targets).*

---

### 🧩 *How It Works*

*The bot continuously:* 
*1. Rotates Browser Fingerprints (Chrome/Safari/Edge) using `curl_cffi`* 
*2. Fetches URLs with randomized delays to mimic human behavior*
*3. Compares live data against MongoDB states* 
*4. Detects user status changes, 403 blocks, or new threads*
*5. Sends Telegram alerts with instant visual feedback* 
*6. Runs a background Flask server for uptime monitoring*

---

### 🚀 *Installation*

```bash
git clone [https://github.com/MyselfNeon/Platinmods](https://github.com/MyselfNeon/Platinmods)
cd Platinmods
pip install -r requirements.txt
```

---

### ⚙️ *Configuration (.env)*

*Create a `.env` file with the following:*

```python
API_ID = 123456
API_HASH = "your_telegram_hash"
BOT_TOKEN = "your_bot_token"

# Database
DB_URI = "mongodb+srv://..."
DB_NAME = "PMT-Testing"

# Owner Configuration (Comma separated IDs)
OWNER_ID = "841851780,7430064956"

# Tuning
MIN_CHECK_INTERVAL = 10
MAX_CHECK_INTERVAL = 20
```

---

### ▶️ *Running the Bot*

```bash
python main.py
```

---

### 🧪 *Commands*

***User Commands:***
**- `/start` *Check Bot Status & Get your ID.***
**- `/check` *Force a manual scan & get system summary.***

***Admin Management (Owner Only):***
**- `/add_user <Name> <URL>` *Add a user to track.***
**- `/del_user <Name>` *Remove a user from tracking.***
**- `/add_forum <Name> <URL>` *Add a forum section to track.***
**- `/del_forum <Name>` *Remove a forum section.***
**- `/auth <ID>` *Authorize a user to receive alerts.***
**- `/unauth <ID>` *Revoke authorization.***
**- `/list` *Show current configuration & targets.***
**- `/restart` *Remotely restart the bot server.***

---

### 🌐 *Deployment*

### *Render / Railway / VPS*

***1. Set `KEEP_ALIVE_URL` in `main.py` (or env)***
***2. Add environment variables (Mongodb, API Keys)***
***3. Deploy via Docker or Python***
***4. Bot stays awake using internal keep-alive task***

---

## ❤️ *Author*

***Neon [MyselfNeon](https://t.me/myselfneon)***
