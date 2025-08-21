# pages/01_Home.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Optional helpers from your scaffold
from src.utils.theme import inject_css
from src.utils.state import ensure_key

st.set_page_config(page_title="BizNexus AI — Home", page_icon="📊", layout="wide")
inject_css("assets/css/style.css")

# ----- Hero -----
st.markdown(
    """
    <div style="padding: 8px 0 2px 0;">
      <h1 style="margin-bottom:4px;">🚀 BizNexus AI</h1>
      <p style="color:#444;margin:0;">
        Your all-in-one AI business analytics — <b>CLV</b> • <b>Churn</b> • <b>Forecast</b> • <b>AI Assistant</b>
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Tip: Load the sample data from **Upload** page to explore features instantly.")

# ----- Metrics (demo-safe) -----
ensure_key("demo_active_customers", 1203)
ensure_key("demo_alerts", 2)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Active Customers", value=f"{st.session_state.get('demo_active_customers', 0):,}")
with m2:
    st.metric("Churn Risk (est.)", value="14.8%", delta="-0.6%")
with m3:
    st.metric("Next 30d Sales (est.)", value="$ 82.3K", delta="+$ 3.1K")
with m4:
    st.metric("Open Alerts", value=st.session_state.get("demo_alerts", 0))

st.markdown("---")

# ----- Quick Actions / Navigation -----
qa1, qa2, qa3, qa4 = st.columns([1,1,1,1])

def page_link(label, page=""):
    # Streamlit 1.32+ has st.page_link; fallback to docs-style link if missing
    try:
        st.page_link(page=page, label=label, icon="👉")
    except Exception:
        st.write(f"👉 **{label}** — open from the sidebar")

with qa1:
    if st.button("📤 Go to Upload"):
        try:
            st.switch_page("pages/03_Upload.py")
        except Exception:
            st.session_state["_nav_fallback"] = "Upload"
    st.caption("Upload your CSV or use the sample data.")

with qa2:
    page_link("🧮 CLV Analysis", "pages/04_CLV.py")
    st.caption("Find high-value customers.")

with qa3:
    page_link("⚠️ Churn Prediction", "pages/05_Churn.py")
    st.caption("Spot at-risk customers.")

with qa4:
    page_link("📈 Sales Forecasting", "pages/06_Forecast.py")
    st.caption("Project short-term revenue.")

st.markdown("---")

# ----- Data awareness + mini chart -----
left, right = st.columns([1.6, 1])

with left:
    st.subheader("📊 Activity Overview")
    if "data" in st.session_state and isinstance(st.session_state["data"], pd.DataFrame):
        df = st.session_state["data"].copy()
        # Normalize basic columns for safety
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        date_col = "purchase_date" if "purchase_date" in df.columns else None
        amt_col = "transaction_amount" if "transaction_amount" in df.columns else None

        if date_col and amt_col:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            daily = (
                df.dropna(subset=[date_col])
                  .groupby(df[date_col].dt.date)[amt_col]
                  .sum()
                  .rename("sales")
                  .to_frame()
            )
            daily.index = pd.to_datetime(daily.index)
            # Ensure a continuous daily index for a smooth area chart
            if not daily.empty:
                full_idx = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
                daily = daily.reindex(full_idx).fillna(0.0)

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=daily.index, y=daily["sales"], mode="lines",
                        fill="tozeroy", name="Sales"
                    )
                )
                fig.update_layout(
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=290,
                    xaxis_title=None, yaxis_title=None
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Data loaded, but no valid dates to chart.")
        else:
            st.info("Data loaded, but expected columns `purchase_date` and `transaction_amount` not found.")
    else:
        st.info("No data yet. Head to **Upload** to load the sample or your CSV.", icon="📤")

with right:
    st.subheader("✨ Highlights")
    st.markdown(
        """
        - **CLV Segments**: Platinum / Gold / Silver
        - **Churn Threshold**: Adjustable alerts
        - **Forecast Uplift**: Simulate promos
        - **Assistant**: Gemini-ready (optional)
        """
    )
    st.markdown(
        """
        **Status**
        - Demo Mode: `{}`  
        - Firebase: `{}`  
        - SMTP: `{}`  
        """.format(
            "on" if (st.secrets.get("app", {}).get("demo_mode", True)) else "off",
            "configured" if "firebase" in st.secrets else "not set",
            "configured" if "email" in st.secrets else "not set",
        )
    )

st.markdown("---")

# ----- Feature cards -----
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("🧮 CLV Analysis")
    st.write("RFM + simple CLV proxy; upgrade-ready to BG/NBD + Gamma-Gamma.")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("⚠️ Churn Prediction")
    st.write("Baseline model now; XGBoost + SHAP explainability next.")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("📈 Sales Forecasting")
    st.write("Rolling average baseline; SARIMA/Prophet coming soon.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----- Footer -----
st.markdown(
    "<div style='text-align:center;color:#888;margin-top:18px;'>"
    "Made with ❤️ for data-driven teams — BizNexus AI"
    "</div>",
    unsafe_allow_html=True,
)
