import streamlit as st
from src.assistant.gemini_client import ask_gemini

st.header("🤖 AI Business Assistant (Demo)")
q = st.text_area("Ask a question", placeholder="e.g., Who are my top 10 customers by CLV?")

if st.button("Ask"):
    answer = ask_gemini(q)
    st.write(answer)
else:
    st.caption("Tip: Configure `[gemini]` in secrets to use the Gemini API; otherwise you'll get a rule-based demo response.")
