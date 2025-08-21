import streamlit as st

def init_state():
    ensure_key("demo_active_customers", 1203)
    ensure_key("demo_alerts", 2)

def ensure_key(key, value):
    if key not in st.session_state:
        st.session_state[key] = value
