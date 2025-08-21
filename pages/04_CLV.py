import streamlit as st
import pandas as pd
import plotly.express as px
from src.models.clv import compute_rfm, simple_clv, add_clv_segments

st.header("🧮 CLV Analysis")

if "data" not in st.session_state:
    st.info("Upload data first on the **Upload** page.", icon="📤")
    st.stop()

df = st.session_state["data"]
rfm = compute_rfm(df, customer_col="customer_id", date_col="purchase_date", amount_col="transaction_amount")

st.subheader("RFM Metrics")
st.dataframe(rfm.head(20), use_container_width=True)

st.subheader("Simple CLV (proxy)")
margin = st.slider("Gross Margin %", 1, 99, 60)
months = st.slider("Forecast Horizon (months)", 1, 36, 12)
retention = st.slider("Expected Monthly Retention %", 50, 99, 85)

clv = simple_clv(rfm, margin_pct=margin/100.0, months=months, retention_pct=retention/100.0)
clv = add_clv_segments(clv)

colA, colB = st.columns([2,1])
with colA:
    st.dataframe(clv.head(30), use_container_width=True)
with colB:
    fig = px.pie(clv, names="segment", title="CLV Segments")
    st.plotly_chart(fig, use_container_width=True)

st.download_button("Download CLV CSV", clv.to_csv(index=False).encode("utf-8"), "clv_results.csv")

import streamlit as st

@st.cache_data(ttl=300)
def compute_rfm(df, customer_col="customer_id", date_col="purchase_date", amount_col="transaction_amount"):
    # ... existing code ...
    return rfm.sort_values("monetary", ascending=False)
