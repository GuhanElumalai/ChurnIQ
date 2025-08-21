import os
import streamlit as st
from src.utils.theme import inject_css
from src.utils.state import init_state


inject_css("assets/css/style.css")
init_state()

st.title("🚀 BizNexus AI")
st.caption("All-in-one AI business analytics — CLV • Churn • Forecasting • Assistant")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Active Customers", value=st.session_state.get("demo_active_customers", 1203))
with col2:
    st.metric("Churn Risk (est.)", value="14.8%")
with col3:
    st.metric("Next 30d Sales (est.)", value="$ 82.3K")
with col4:
    st.metric("Alerts", value=st.session_state.get("demo_alerts", 2))

st.markdown("---")
st.subheader("Quick Start")
st.write("• Upload sample data on **Upload** page → Explore **CLV**, **Churn**, and **Forecast** pages.")
st.write("• Configure services in **Settings** → then switch off Demo Mode.")
st.info("Tip: This starter works without any secrets. When you're ready, fill `.streamlit/secrets.toml`.", icon="💡")
