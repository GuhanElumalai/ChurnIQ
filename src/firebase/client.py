import os
import streamlit as st

def get_firebase_config():
    try:
        cfg = st.secrets["firebase"]["config"]
        return dict(cfg)
    except Exception:
        return None
