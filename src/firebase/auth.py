import streamlit as st
import pyrebase

def init_firebase():
    config = st.secrets["firebase.config"]
    firebase = pyrebase.initialize_app(config)
    return firebase.auth()

def signup_user(email, password):
    auth = init_firebase()
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user
    except Exception as e:
        return {"error": str(e)}

def login_user(email, password):
    auth = init_firebase()
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.session_state["user"] = user
        return user
    except Exception as e:
        return {"error": str(e)}

def logout_user():
    if "user" in st.session_state:
        del st.session_state["user"]
