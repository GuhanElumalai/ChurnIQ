import streamlit as st

def _gemini_available():
    try:
        key = st.secrets["gemini"]["api_key"]
        return bool(key and len(key) > 10)
    except Exception:
        return False

def ask_gemini(question: str) -> str:
    if not _gemini_available():
        q = (question or "").lower()
        if "top" in q and "customer" in q:
            return "Demo: Top customers by CLV — C0009, C0017, C0004 ..."
        if "forecast" in q:
            return "Demo: Next month's forecast is ~ $82K."
        return "Demo: Add [gemini] api_key in secrets to enable the AI assistant."

    import google.generativeai as genai
    genai.configure(api_key=st.secrets["gemini"]["api_key"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""You are an AI business analyst. Answer succinctly.
    User question: {question}
    If data is needed, explain what to compute from columns: customer_id, purchase_date, transaction_amount, product_id, region."""
    resp = model.generate_content(prompt)
    try:
        return resp.text
    except Exception:
        return "Gemini: Received a response but couldn't parse text."
