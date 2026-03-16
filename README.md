## *Save Restricted Content Bot*
***Live Bot: [@SaveRestrictions_oBot](https://t.me/SaveRestrictions_oBot) | Updates: [@NeonFiles](https://t.me/NeonFiles)***

### 📌 *Core System Updates*
- ***100% Free Hybrid Credit System**: Paid plans removed. Uses an ad-supported token system.*
- ***Temporary Credits**: Users verify via shortlinks (`/token`) to get 3-hour temporary credits.*
- ***Permanent Credits**: Admins can grant non-expiring credits directly to users.*
- ***Anti-Hoarding**: Built-in reset (`/newtoken`) prevents token stacking and ad bypass.*

### 🚀 *Key Features*
- ***Extract Anywhere**: Save restricted content from public/private channels and bots.*
- ***Smart Login**: Session-based login (`/login`) with phone number support.*
- ***Media Customization**: Custom captions, custom thumbnails, and automatic word replacement.*
- ***Multi-Downloader**: Download media from YouTube, Instagram, Facebook, Twitter (yt-dlp).*
- ***Heavy Uploads**: 4GB file upload support (if a premium session string is added).*
- ***Fast Uploading**: Powered by Pyrogram v2 + SpyLib + Telethon.*

### ⚡ *Main Commands*
- `/start` - *Start the bot.*
- `/login` & `/logout` - *Manage your account session.*
- `/token` - *Get 3 hours of free access via shortlink.*
- `/newtoken` - *Reset active token to verify again.*
- `/mycredits` - *Check remaining credits & expiration time.*
- `/batch` - *Extract files in bulk.*
- `/addcredits` *[id] [amount] - (Admin) Grant permanent credits.*
- `/remcredits` *[id] [amount] - (Admin) Remove permanent credits.*

### ⚙️ *Required Variables*
- `API_ID` & `API_HASH` - *From my.telegram.org.*
- `BOT_TOKEN` - *From @BotFather.*
- `OWNER_ID` - *Your Telegram User ID.*
- `MONGO_DB` - *Database URL for sessions, tokens, and credits.*
- `LOG_GROUP` - *Channel/Group ID for logging new users & verifications.*
- `CHANNEL_ID` - *Channel ID for forced subscription.*
- `WEBSITE_URL` - *Shortlink domain (e.g., `upshrink.com`) for the token system.*
- `AD_API` - *API key for your shortlink dashboard.*
- `VERIFY_CREDITS` - *Amount of credits given per token verification (Default: `10`).*

### 🏆 *Credits*
- ***Developer**: [MyselfNeon](https://github.com/MyselfNeon/)*
