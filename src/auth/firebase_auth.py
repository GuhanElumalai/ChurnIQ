import streamlit as st
import requests

def is_demo() -> bool:
    try:
        return bool(st.secrets["app"]["demo_mode"])
    except Exception:
        return True

def _api_key():
    try:
        return st.secrets["firebase"]["config"]["apiKey"]
    except Exception:
        return None

def signup_user(email: str, password: str):
    if is_demo(): return True, "Demo signup ok"
    key = _api_key()
    if not key: return False, "Firebase apiKey missing"
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={key}"
    r = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
    if r.ok: return True, "Signed up"
    return False, r.json().get("error", {}).get("message", "Signup failed")

def login_user(email: str, password: str):
    if is_demo(): return True, "Demo login ok"
    key = _api_key()
    if not key: return False, "Firebase apiKey missing"
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={key}"
    r = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
    if r.ok:
        data = r.json()
        st.session_state["id_token"] = data["idToken"]
        st.session_state["refresh_token"] = data.get("refreshToken")
        return True, "Logged in"
    return False, r.json().get("error", {}).get("message", "Login failed")
