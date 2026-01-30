def check_account(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    
    try:
        r = requests.post(url, json=payload, timeout=10)
        data = r.json()
        
        if r.status_code == 200:
            return "LIVE"
        
        # Sadece "BAD" deme, Google'ın gerçek hatasını bize söyle
        return data.get('error', {}).get('message', 'BAD') 
    except Exception:
        return "SISTEM_HATASI"
