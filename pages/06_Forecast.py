import streamlit as st
import pandas as pd
from src.models.forecast import aggregate_daily_sales, rolling_forecast
import plotly.graph_objects as go

st.header("📈 Sales Forecasting (Rolling Average)")

if "data" not in st.session_state:
    st.info("Upload data first on the **Upload** page.", icon="📤")
    st.stop()

df = st.session_state["data"]
daily = aggregate_daily_sales(df, date_col="purchase_date", amount_col="transaction_amount")
window = st.slider("Rolling Window (days)", 3, 28, 7)
horizon = st.slider("Forecast Horizon (days)", 7, 60, 30)

hist, fc = rolling_forecast(daily, window=window, horizon=horizon)

fig = go.Figure()
fig.add_scatter(x=hist.index, y=hist.values, mode="lines", name="History")
fig.add_scatter(x=fc.index, y=fc.values, mode="lines", name="Forecast")
st.plotly_chart(fig, use_container_width=True)

# after computing hist, fc ...
uplift = st.slider("Promo Uplift (%) on forecast", 0, 100, 0, 5)
if uplift > 0:
    fc = fc * (1 + uplift/100.0)

