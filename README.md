### *GDrive Authorization Redirect 🔐*

*A stylish, responsive authorization page designed for the `@NeonGDriveBot` Telegram bot. This page extracts authentication codes from the URL, presents them securely, and provides a seamless one-click copy and redirect experience back to Telegram.*

### *✨ Features*
*- **URL Parameter Extraction:** Automatically fetches the `?code=` query parameter.*  
*- **1-Click Copy & Redirect:** Users can click a single button to copy the auth code to their clipboard and immediately open the Telegram bot.*  
*- **Dynamic Backgrounds:** Randomly selects background images from a curated list or fetches dynamically from the `waifu.pics` API.*  
*- **Glassmorphism Card:** A clean, blurred UI aesthetic focusing on the user action.*  
*- **Mobile-Locked UI:** Disables touch scrolling and zooming to feel like a native app screen.*

### ⚙️ *How It Works*
***01.** A user authenticates via a third-party service (e.g., Google Drive OAuth).*  
***02.** The service redirects to this hosted page, appending the auth code: `https://yourdomain.com/?code=4/0AX4Xf...`*  
***03.** The JavaScript on this page parses the URL and displays the code.*
*04. Clicking the **COPY & REDIRECT TO BOT** button copies the code and triggers a window redirect to `https://t.me/NeonGDriveBot`.*

### 🚀 *Deployment*
*This project is entirely static (`index.html` and `styles.css`). 
Deploy it to a static host (GitHub Pages, Cloudflare Pages, Netlify) and set the resulting URL as your OAuth redirect URI in the Google Cloud Console.*

### 🛠️ *Customization*
*- **Bot Username:** Change the `BOT_USERNAME` constant in the JavaScript block inside `index.html` to link to a different Telegram bot.*  
*- **Background Images:** Modify the `imageLinksString` string in the script to add or remove custom direct image links.*
