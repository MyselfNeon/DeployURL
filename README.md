### Website Monitor Bot 🌐

***Advanced Automated Monitoring Bot built with Pyrogram, Flask, and MongoDB. Designed to bypass Cloudflare protections using TLS Fingerprinting **(`curl_cffi`)** to track user statuses and forum activity in real-time.***

---

### ✨ Key Features

### 🛡️ ***Advanced Scraping***
* ***Cloudflare Bypass:** Uses `curl_cffi` to impersonate real browsers (Chrome 120 / Safari 17) and bypass 403 Forbidden errors.*
* ***Smart Throttling:** Implements random delays (`REQUEST_DELAY`) and session rotation to mimic human behavior.*
* ***Auto-Warmup:** "Warms up" sessions by visiting homepages before scraping specific targets.*

### 📊 **Data & Analytics**
* ***MongoDB Database:** Persistent storage for targets, authorization, and activity logs (replaces JSON).*
* ***Activity Graphs:** Generates hourly activity graphs for tracked users via `/activity` (7-day history retention).*
* ***IST Time Support:** Automatically converts server time to Indian Standard Time (IST) for status reports.*

### 🤖 **Bot Management**
* ***Dynamic Configuration:** Add or remove users/forums directly via Telegram commands—no code edits required.*
* ***Owner Security:** Strict `OWNER_ID` and Admin Authorization system (`/auth`) to prevent unauthorized access.*
* ***Web Dashboard:** Integrated Flask server with a "Neon" themed health-check page and Keep-Alive support.*

### 🛠️ Tech Stack

* ***Python 3.10+***
* ***Pyrogram:** Telegram MTProto API Client.*
* ***Motor:** Asynchronous MongoDB driver.*
* ***Curl_CFFI:** TLS Fingerprinting for scraping.*
* ***Flask:** Web server for deployment health checks.*
* ***BeautifulSoup4:** HTML Parsing.*

### 🚀 Installation

<details><summary><b><i>Installation Guide</i></summary></b>

1.  ***Clone the Repository***
    ```bash
    git clone [https://github.com/MyselfNeon/Website-Monitor.git](https://github.com/MyselfNeon/Website-Monitor.git)
    cd Website-Monitor
    ```

2.  ***Install Dependencies***
    ```bash
    pip install -r requirements.txt
    ```

3.  ***Set Up Environment Variables***
    *Create a `.env` file in the root directory and add the following:*

    ```ini
    # Telegram API (my.telegram.org)
    API_ID=123456
    API_HASH=your_api_hash
    BOT_TOKEN=your_bot_token

    # Admin Configuration
    OWNER_ID=123456789,987654321

    # Database (MongoDB Connection String)
    DB_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
    DB_NAME=PMT-Testing

    # Application Settings
    MIN_CHECK_INTERVAL=60
    MAX_CHECK_INTERVAL=120
    PORT=8080
    ```

4.  ***Run the Bot***
    ```bash
    python main.py
    ```

</details>

### *Config Variables ➠*

<details><summary><b><i>ENV Variables</i></summary></b>

#### *Mandatory Variables ➠*

* [`API_ID`]: ***From [My Telegram](https://my.telegram.org).***
* [`API_HASH`]: ***From [My Telegram](https://my.telegram.org).***
* [`ADMIN`]: ***Your Telegram User ID. Get From [@MissRose_Bot](https://t.me/MissRose_Bot)***
* [`BOT_TOKEN`]: ***Telegram API Bot Token, Get it from [@BotFather](https://t.me/BotFather).***
* [`DB_NAME`]: ***DataBase Name Optional. Default to UptimeBot.***
* [`DB_URI`]: ***[MongoDB URI](https://cloud.mongodb.com) for Saving Urls and History by User.***
* [`PORT`]: ***Web Server Port. Optional Defaults to `8080`.***

</details>

### *Bot Commands ➠* 

<details><summary><b><i>Bot Commands</i></b></summary>
  
```
start - Check bot status and get your Chat ID
check -  Force a manual scrape and get a summary report
add_user <Name> <URL> - Add a user profile to the tracking list
del_user <Name> - Remove a user from the tracking list
add_forum <Name> <URL> - Add a forum section to monitor for new threads
del_forum <Name> - Remove a forum from the tracking list
activity <Name> - Generate an hourly activity graph for a user
list - Show all tracked users, forums, and authorized IDs.
auth <UID> - Authorize a user to receive alerts and use /check.
unauth <UID> - Revoke authorization from a user.
restart - Restart the bot process remotely
```
<b><i>• Copy all Commands and paste it in <a href='https://t.me/botfather'>BotFather</a> to apply Commands.

</details>

### 🌐 Cloud Deployment

***This bot is optimized for cloud deployment.***

1.  ***Flask Keep-Alive:** The bot runs a web server on `0.0.0.0` (Port 8080 by default).*
2.  ***Health Check:** Accessing the root URL (`/`) displays a styled Neon HTML page confirming the bot is online.*
3.  ***Self-Pinging:** Configure `KEEP_ALIVE_URL` in `main.py` (or via env vars) to ping itself every 5 minutes to prevent sleeping.*

### ⚠️ Disclaimer

***This tool is for **educational purposes only**. The scraping mechanism includes delays to be respectful to the target server. The author is not responsible for any misuse or IP bans resulting from the use of this bot.***

---

### ❤️ Credits

**Developer:** [MyselfNeon](https://t.me/MyselfNeon)  
**GitHub:** [MyselfNeon](https://github.com/MyselfNeon/)
