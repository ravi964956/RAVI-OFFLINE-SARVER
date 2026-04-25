import requests
import time
import threading
import os
import datetime
import random
import string
import sys
import uuid
from flask import Flask, render_template_string, request, jsonify, session

# --- 🕒 TIMEZONE SETUP (INDIA) 🕒 ---
try:
    import pytz
    KOLKATA = pytz.timezone('Asia/Kolkata')
except ImportError:
    KOLKATA = None

# --- 🔒 ULTRA-MAX SECURITY SHIELD (RAVI KUMAR PRAJAPAT) 🔒 ---
A = "MR. RAVI KUMAR PRAJAPAT"
B = "RAVI KUMAR POST COMMENTS SERVER"
C = "61573328623221"

def secure_check():
    if A != "MR. RAVI KUMAR PRAJAPAT" or B != "RAVI KUMAR POST COMMENTS SERVER" or C != "61573328623221":
        return False
    return True

if not secure_check():
    sys.exit("🛑 SECURITY ALERT: FILE TAMPERED!")

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Global Variables
render_start_time = datetime.datetime.now(KOLKATA) if KOLKATA else datetime.datetime.now()
user_data = {} 
total_active_users = 0

def get_now_time():
    if KOLKATA:
        return datetime.datetime.now(KOLKATA).strftime("%I:%M:%S %p")
    return datetime.datetime.now().strftime("%I:%M:%S %p")

def add_user_log(user_id, status_msg, post_id, actual_msg, color="#0f0"):
    if user_id in user_data:
        now = get_now_time()
        border = "❉═══════RK-PRAJAPAT════════❉"
        log_entry = (
            f"<div style='color:{color}; margin-bottom:10px; font-weight:bold;'>"
            f"{border}<br>USER :- {status_msg}<br>POST ID :- {post_id}<br>COMMENT :- {actual_msg}<br>"
            f"TIME :- {now}<br>{border}</div>"
        )
        user_data[user_id]['logs'].append(log_entry)
        if len(user_data[user_id]['logs']) > 30: user_data[user_id]['logs'].pop(0)

# --- 🚀 PREMIUM HTML DASHBOARD 🚀 ---
HTML_DASHBOARD = f"""
<!DOCTYPE html>
<html>
<head>
    <title>POST COMMENTS SERVER - {A}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ background-color: #ffb6c1; color: #000; font-family: 'Poppins', sans-serif; text-align: center; margin: 0; padding: 10px; }}
        .gold-name {{ color: #FFD700; font-size: 26px; font-weight: bold; text-shadow: 2px 2px 4px #000; margin-top: 10px; }}
        .blue-sub {{ color: #0000FF; font-size: 13px; font-weight: bold; margin-bottom: 2px; display: block; }}
        
        .monitor-box {{ background: #000; color: #fff; border-radius: 20px; border: 3px solid #ff1493; padding: 15px; width: 92%; max-width: 500px; margin: 15px auto; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }}
        .monitor-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 10px 0; }}
        .m-item {{ font-weight: bold; font-size: 13px; text-transform: uppercase; }}
        .m-value {{ color: #fff; display: block; margin-top: 3px; font-size: 15px; }}
        
        .dp-container {{ margin: 10px auto; width: 110px; height: 110px; border-radius: 50%; border: 4px solid #fff; overflow: hidden; box-shadow: 0 0 20px #ff1493; }}
        .dp-container img {{ width: 100%; height: 100%; object-fit: cover; }}
        
        .container {{ background: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 25px; border: 3px solid #ff1493; display: inline-block; width: 95%; max-width: 600px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .box {{ padding: 12px; margin: 8px 0; border-radius: 12px; font-weight: bold; border: 2px solid #fff; color: #fff; text-shadow: 1px 1px 2px #000; }}
        
        input, textarea {{ width: 92%; padding: 12px; margin: 5px 0; border-radius: 10px; border: 1px solid #ccc; font-size: 14px; outline: none; }}
        .btn-start {{ background: linear-gradient(to right, #ff1493, #ff69b4); color: #fff; padding: 15px; border: none; cursor: pointer; font-weight: bold; width: 95%; border-radius: 12px; font-size: 18px; margin-top: 10px; }}
        .btn-stop {{ background: #000; color: #fff; padding: 15px; border: none; cursor: pointer; font-weight: bold; width: 95%; border-radius: 12px; margin-top: 10px; }}
        
        #console {{ background: #1a1a1a; color: #0f0; text-align: left; padding: 15px; height: 300px; overflow-y: auto; border: 2px solid #ff1493; font-family: monospace; font-size: 11px; margin-top: 20px; border-radius: 12px; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <div id="main-content">
        <div class="dp-container"><img src="https://i.postimg.cc/4xqSYF3V/IMG-20260306-225423.png"></div>
        <div class="gold-name">{A}</div>
        <div class="blue-sub">{B}</div>
        
        <div class="monitor-box">
            <h3 style="color: #ff1493; margin: 0 0 10px 0;">❉═══ RK-PRAJAPAT LIVE ═══❉</h3>
            <div class="monitor-grid">
                <div class="m-item" style="color: #00bfff;">🕒 UPTIME <br><span class="m-value" id="srv_up">0h 0m 0s</span></div>
                <div class="m-item" style="color: #ffff00;">👤 ACTIVE <br><span class="m-value" id="act_u">0</span></div>
                <div class="m-item" style="color: #32cd32;">✅ SENT <br><span class="m-value" id="s_cnt">0</span></div>
                <div class="m-item" style="color: #ff0000;">❌ FAILED <br><span class="m-value" id="f_cnt">0</span></div>
            </div>
            <h3 style="color: #ff1493; margin: 10px 0 0 0;">❉══════════════════❉</h3>
        </div>

        <div class="container">
            <div id="tokenBox" style="background:#ffff00; padding:10px; margin-bottom:10px; display:none; border-radius:10px; font-weight:bold; border: 2px solid #000; color:#000;">
                STOP CODE: <span id="stopCode">---</span>
            </div>
            
            <form id="botForm">
                <div class="box" style="background:#4b0082;">🔑 MULTI TOKENS (One per line)</div>
                <textarea id="tokenInput" placeholder="Paste Access Tokens here..." rows="4" required></textarea>
                
                <div class="box" style="background:#00bfff;">🆔 FACEBOOK POST ID</div>
                <input type="text" id="post_id" placeholder="Enter Post Link or ID..." required>
                
                <div class="box" style="background:#9370db;">👤 HATER NAME</div>
                <input type="text" id="hater_name" placeholder="Name for Comment..." required>
                
                <div class="box" style="background:#ffa500;">📤 COMMENTS FILE (.TXT)</div>
                <input type="file" id="fileInput" accept=".txt">
                
                <div class="box" style="background:#32cd32;">⚡ SPEED (SECONDS)</div>
                <input type="number" id="speed" value="10" required min="1">
                
                <button type="button" class="btn-start" onclick="startBot()">🚀 START COMMENT SERVER</button>
                <button type="button" class="btn-stop" onclick="stopBot()">🛑 STOP TASK SYSTEM</button>
                <input type="text" id="stop_input" placeholder="Enter STOP CODE..." style="margin-top:10px; background:#222; color:#fff;">
            </form>
            
            <div id="console">⌨️ CONSOLE LOG READY...</div>
        </div>
    </div>

    <script>
        let uploadedMessages = "";
        document.getElementById('fileInput').addEventListener('change', function(e) {{
            const reader = new FileReader();
            reader.onload = function(e) {{ uploadedMessages = e.target.result; }};
            reader.readAsText(e.target.files[0]);
        }});

        function startBot() {{
            const tokens = document.getElementById('tokenInput').value;
            const post = document.getElementById('post_id').value;
            const name = document.getElementById('hater_name').value;
            const spd = document.getElementById('speed').value;
            
            if(!tokens || !post || !uploadedMessages) {{ alert("Fill all details!"); return; }}

            const data = {{ post_id: post, hater_name: name, tokens: tokens, messages: uploadedMessages, speed: spd }};
            fetch('/start', {{ method: 'POST', headers: {{'Content-Type': 'application/json'}}, body: JSON.stringify(data) }})
            .then(res => res.json()).then(resData => {{
                document.getElementById('tokenBox').style.display = 'block';
                document.getElementById('stopCode').innerText = resData.token;
            }});
        }}

        function stopBot() {{
            const code = document.getElementById('stop_input').value;
            fetch('/stop', {{ method: 'POST', headers: {{'Content-Type': 'application/json'}}, body: JSON.stringify({{code: code}}) }})
            .then(res => res.json()).then(data => alert(data.message));
        }}

        function updateUI() {{
            fetch('/status').then(res => res.json()).then(data => {{
                document.getElementById('srv_up').innerText = data.server_up;
                document.getElementById('act_u').innerText = data.active;
                document.getElementById('s_cnt').innerText = data.sent;
                document.getElementById('f_cnt').innerText = data.failed;
                document.getElementById('console').innerHTML = data.logs.join('');
                const c = document.getElementById('console'); c.scrollTop = c.scrollHeight;
            }});
        }}
        setInterval(updateUI, 2000);
    </script>
</body>
</html>
"""

def comment_sender(user_id, post_id, hater_name, tokens_list, messages, speed):
    msg_list = messages.splitlines()
    num_tokens = len(tokens_list)
    
    while user_data.get(user_id, {}).get('running'):
        for i, msg in enumerate(msg_list):
            if not user_data.get(user_id, {}).get('running'): break
            
            current_token = tokens_list[i % num_tokens].strip()
            
            try:
                # FB API for Posting Comments
                url = f"https://graph.facebook.com/v17.0/{{post_id}}/comments"
                payload = {{'message': f"{{hater_name}} {{msg.strip()}}", 'access_token': current_token}}
                res = requests.post(url, json=payload)
                
                if res.ok:
                    user_data[user_id]['sent'] += 1
                    add_user_log(user_id, hater_name, post_id, msg.strip())
                else:
                    user_data[user_id]['failed'] += 1
                    add_user_log(user_id, "FAILED", post_id, "ERROR IN TOKEN OR POST ID!", color="#f00")
            except:
                user_data[user_id]['failed'] += 1
                add_user_log(user_id, "ERROR", post_id, "NETWORK ERROR!", color="#f00")
            
            time.sleep(int(speed))

@app.route('/')
def index():
    global total_active_users
    if 'user_id' not in session: 
        session['user_id'] = str(uuid.uuid4())
        total_active_users += 1
    uid = session['user_id']
    if uid not in user_data: user_data[uid] = {'running': False, 'sent': 0, 'failed': 0, 'logs': [], 'stop_token': ""}
    return render_template_string(HTML_DASHBOARD)

@app.route('/status')
def get_status():
    uid = session.get('user_id')
    now = datetime.datetime.now(KOLKATA) if KOLKATA else datetime.datetime.now()
    srv_upt = str(now - render_start_time).split('.')[0]
    u = user_data.get(uid, {'sent':0, 'failed':0, 'logs':[], 'running':False})
    return jsonify(server_up=srv_upt, active=total_active_users, sent=u['sent'], failed=u['failed'], logs=u['logs'])

@app.route('/start', methods=['POST'])
def start():
    uid = session.get('user_id')
    data = request.json
    s_token = "RK-POST-" + ''.join(random.choices(string.digits, k=4))
    
    tokens_list = data.get('tokens').splitlines()
    user_data[uid].update({'running': True, 'sent': 0, 'failed': 0, 'logs': ["🚀 Comment Server Live!"], 'stop_token': s_token})
    
    threading.Thread(target=comment_sender, args=(uid, data.get('post_id'), data.get('hater_name'), tokens_list, data.get('messages'), data['speed'])).start()
    return jsonify(token=s_token)

@app.route('/stop', methods=['POST'])
def stop():
    uid = session.get('user_id')
    if request.json.get('code') == user_data[uid]['stop_token']:
        user_data[uid]['running'] = False
        return jsonify(message="🛑 Commenting Stopped!")
    return jsonify(message="❌ Wrong Stop Code!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
