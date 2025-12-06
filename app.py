# ------------------------------------------------
# File Name: App.py
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# Last Modified: 2025-10-21
# ------------------------------------------------

from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def health_check():
    # Returning the full HTML content for the health check endpoint
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>@MyselfNeon</title>
  <style>
    body {
      background-color: black;
      margin: 0;
      height: 100vh;
      font-family: 'Brush Script MT', cursive;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      text-align: center;
      overflow: hidden;
      padding-top: 20vh;
    }

    /* Added avatar + neon cyan glow */
    .avatar {
      width: 150px;
      height: 150px;
      border-radius: 50%;
      margin-bottom: 25px;
      box-shadow:
        0 0 8px #00eaff,
        0 0 15px #00eaff,
        0 0 30px #00eaff;
    }

    a {
      text-decoration: none;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: auto;
      width: 100%;
      cursor: pointer;
    }

    h1 {
      font-size: clamp(2.5rem, 8vw, 7rem);
      letter-spacing: 2px;
      margin-bottom: 0.3rem;
      animation: redToBlue 2s infinite alternate ease-in-out;
      text-shadow:
        0 0 1px currentColor,
        0 0 3px currentColor;
    }

    h2 {
      font-size: clamp(1.8rem, 6vw, 4.8rem);
      letter-spacing: 2px;
      color: #39FF14;
      text-shadow:
        0 0 1px #39FF14,
        0 0 3px #00FF00;
    }

    @keyframes redToBlue {
      0% { color: #FF2400; }
      50% { color: #FF1493; }
      100% { color: #00BFFF; }
    }
  </style>
</head>
<body>

  <img class="avatar" src="https://avatars.githubusercontent.com/u/194442566?v=4" alt="MyselfNeon Avatar">

  <a href="https://t.me/nWebAlertsBot" target="_blank">
    <h1>Web Alerts Bot</h1>
    <h2>Coded By @MyselfNeon</h2>
  </a>
  
  <p style="color: white; margin-top: 50px;">
    Bot Status: <span style="color: #39FF14;">Online & Monitoring</span>
  </p>

</body>
</html>"""

def run_web_server(port):
    """Runs the Flask app in a separate thread."""
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

def start_web_server(port):
    """Helper to start the server thread."""
    t = threading.Thread(target=run_web_server, args=(port,))
    t.daemon = True
    t.start()
    
