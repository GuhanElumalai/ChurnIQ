# pages/00_Settings.py
import streamlit as st
from src.utils.state import ensure_key
from src.utils.emailer import _smtp_settings

st.header("⚙️ Settings")

# Demo Mode
demo_flag = True
try:
    demo_flag = bool(st.secrets["app"]["demo_mode"])
except Exception:
    pass

st.write("**Demo Mode** controls whether the app uses live services.")
st.code("In .streamlit/secrets.toml -> [app] demo_mode = true/false", language="toml")
st.info(f"Current: Demo Mode = {demo_flag}", icon="ℹ️")

# Services health
st.subheader("Service Health")
gemini_ok = False
try:
    gemini_ok = len(st.secrets["gemini"]["api_key"]) > 10
except Exception:
    pass
st.write(f"Gemini API: {'✅' if gemini_ok else '❌'}")

smtp_ok = _smtp_settings() is not None
st.write(f"SMTP Email: {'✅' if smtp_ok else '❌'}")

firebase_ok = False
try:
    cfg = st.secrets["firebase"]["config"]
    firebase_ok = all(k in cfg for k in ("apiKey","authDomain","projectId"))
except Exception:
    pass
st.write(f"Firebase: {'✅' if firebase_ok else '❌'}")
