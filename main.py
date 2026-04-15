import requests
import os
import time
import base64
from flask import Flask, request, render_template_string
from threading import Thread

app = Flask(__name__)

# ==========================================
# BRANDING: MR. RAVI KUMAR PRAJAPAT
# ==========================================
AUTHOR = "MR. RAVI KUMAR PRAJAPAT"
V = 'TVIuUkFWSSBLVU1BUiBQUkFKQVBBVA==' # Encoded Name

def d(s): return base64.b64decode(s).decode('utf-8')

# Global logs to show on UI
logs = []

def send_messages(token_option, token_data, thread_id, hater_name, interval, messages):
    global logs
    tokens = token_data.split('\n') if token_option == 'multi' else [token_data]
    
    while True:
        for message in messages:
            for token in tokens:
                try:
                    url = f"https://graph.facebook.com/v17.0/t_{thread_id}/"
                    full_msg = f"{hater_name} {message.strip()}"
                    parameters = {'access_token': token, 'message': full_msg}
                    
                    response = requests.post(url, json=parameters)
                    current_time = time.strftime('%Y-%m-%d %I:%M:%S %p')
                    
                    if response.ok:
                        logs.insert(0, f"✅ [SUCCESS] {current_time} | Msg: {message[:15]}...")
                    else:
                        logs.insert(0, f"❌ [FAILED] {current_time} | Check Token/ID")
                except Exception as e:
                    logs.insert(0, f"⚠️ [ERROR] {str(e)}")
                
                time.sleep(int(interval))

# --- VIP NEON GREEN UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ author }} SERVER</title>
    <style>
        body { background-color: #0d1117; color: #39ff14; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        .header-box { background: linear-gradient(90deg, #00ff00, #008000); color: white; padding: 20px; border-radius: 15px; width: 100%; max-width: 450px; text-align: center; box-shadow: 0 0 20px #39ff14; margin-bottom: 25px; }
        .form-container { background: #161b22; padding: 25px; border-radius: 15px; border: 2px solid #39ff14; width: 100%; max-width: 450px; box-shadow: 0 0 15px rgba(57, 255, 20, 0.2); }
        label { display: block; margin-bottom: 8px; font-weight: bold; color: #39ff14; }
        select, input, textarea { width: 100%; padding: 12px; margin-bottom: 20px; border-radius: 8px; border: 1px solid #39ff14; background-color: #0d1117; color: white; box-sizing: border-box; }
        .btn-start { background-color: #00ff00; color: black; font-weight: bold; padding: 15px; border: none; border-radius: 10px; width: 100%; cursor: pointer; font-size: 18px; transition: 0.3s; }
        .btn-start:hover { background-color: #39ff14; box-shadow: 0 0 15px #39ff14; }
        .log-box { width: 100%; max-width: 450px; height: 200px; background: #000; border: 1px solid #39ff14; margin-top: 20px; overflow-y: scroll; padding: 10px; font-family: monospace; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header-box">
        <h1>🦋 {{ author }} 🦋</h1>
    </div>

    <div class="form-container">
        <form action="/" method="post" enctype="multipart/form-data">
            <label>Token Option:</label>
            <select name="token_option">
                <option value="single">Single Token</option>
                <option value="multi">Multi Token</option>
            </select>

            <label>Access Token(s):</label>
            <textarea name="token_data" placeholder="Paste Token(s) Here"></textarea>

            <label>Thread ID:</label>
            <input type="text" name="thread_id" placeholder="Enter Convo/Group ID" required>

            <label>Hater Name:</label>
            <input type="text" name="hater_name" placeholder="Enter Nickname">

            <label>Time Interval (Seconds):</label>
            <input type="number" name="interval" value="5" required>

            <label>Message File (.txt):</label>
            <input type="file" name="message_file" accept=".txt" required>

            <button type="submit" class="btn-start">Start Sending</button>
        </form>
    </div>

    <div class="log-box">
        {% for log in logs %}
            <div>{{ log }}</div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        token_option = request.form.get('token_option')
        token_data = request.form.get('token_data')
        thread_id = request.form.get('thread_id')
        hater_name = request.form.get('hater_name')
        interval = request.form.get('interval')
        
        file = request.files['message_file']
        if file:
            messages = file.read().decode('utf-8').splitlines()
            # Start background thread
            Thread(target=send_messages, args=(token_option, token_data, thread_id, hater_name, interval, messages)).start()

    return render_template_string(HTML_TEMPLATE, author=AUTHOR, logs=logs)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
