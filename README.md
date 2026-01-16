## *Website Monitor Bot* 🌐

*A fully automated, stealthy monitoring bot for Websites built using Pyrogram curl_cffi (Browser Impersonation), MongoDB (Motor), Flask, and asynchronous scraping with BeautifulSoup.*

---

### ✨ *Features*

- *User Online/Offline tracking*
- *New forum thread detection & removed thread alerts*
- *Advanced Anti-Detection (Browser Impersonation & Random Delays)*
- *Auto-Healing for notmal Errors*
- *Full Admin Management via Telegram (Add/Remove targets dynamically)*
- *MongoDB Database support for persistent state tracking*
- *In memory to avoid duplicate alerts.*
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
***1.** Rotates Browser Fingerprints (Chrome/Safari/Edge) using `curl_cffi`*  
***2.** Fetches URLs with randomized delays to mimic human behavior*  
***3.** Compares live data against MongoDB*  
***4.** Detects user status changes, 403 blocks, or new threads*  
***5.** Sends Telegram alerts with instant visual feedback*  
***6.** Runs a background Flask server for uptime monitoring*  

---

### 🚀 *Installation*

```bash
git clone [https://github.com/MyselfNeon/Platinmods](https://github.com/MyselfNeon/Platinmods)
cd Platinmods
pip install -r requirements.txt
```

---

### ⚙️ *Configuration (.env)*

<details><summary><b>Variables</summary></b></summary>

* [`API_ID`] - _**From  <a href='https://my.telegram.org/'>TG Auth**_</a>
* [`API_HASH`] - _**From <a href='https://my.telegram.org/'>TG Auth**_</a>
* [`BOT_TOKEN`] - _**From <a href='https://t.me/botfather'>BotFather**_</a>
* [`OWNER_ID`] - **_ID of Admin._**
* [`DB_URI`] - _**Give Your<a href='https://cloud.mongodb.com/'> MongoDB Url**_
</details>

---

### ▶️ *Running the Bot*

```bash
python main.py
```

---

### 🧪 *Commands*

```
start - Check Bot status and get ID
check - Force a Manual scan
add_user - Add user to track
del_user - Remove User from Tracking
add_forum - Add forum to track
del_forum - Remove forum from Tracking
auth - Authorize a user
unauth - Revoke user
list - Show current config
restart - Restart bot servers
```
***Copy all Commands and set it manually inside [Botfather](https://t.me/Botfather) or use `/setcmd` after deploy to set commands Automatically***

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
