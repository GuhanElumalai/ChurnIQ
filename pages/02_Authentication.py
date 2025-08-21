import streamlit as st
from src.firebase.auth import signup_user, login_user, logout_user

st.title("🔐 Authentication")

if "user" in st.session_state:
    st.success(f"Logged in as: {st.session_state['user']['email']}")
    if st.button("Logout"):
        logout_user()
        st.rerun()
else:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            result = login_user(login_email, login_password)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Login successful ✅")
                st.rerun()

    with tab2:
        st.subheader("Sign Up")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up"):
            result = signup_user(signup_email, signup_password)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Account created ✅ Please log in.")
