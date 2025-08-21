import streamlit as st
from src.models.churn import build_features, train_baseline, infer_probabilities
import joblib, os

st.header("⚠️ Churn Prediction (Baseline)")

if "data" not in st.session_state:
    st.info("Upload data first on the **Upload** page.", icon="📤")
    st.stop()

df = st.session_state["data"]
X, y = build_features(df)

cache_dir = ".cache"
os.makedirs(cache_dir, exist_ok=True)
model_path = os.path.join(cache_dir, "churn_baseline.joblib")

if st.button("Train / Retrain Model"):
    model, metrics = train_baseline(X, y)
    joblib.dump({"model":model, "metrics":metrics}, model_path)
    st.success("Model trained and cached.", icon="✅")

payload = None
if os.path.exists(model_path):
    payload = joblib.load(model_path)
else:
    # train once automatically
    model, metrics = train_baseline(X, y)
    joblib.dump({"model":model, "metrics":metrics}, model_path)
    payload = {"model":model, "metrics":metrics}

st.subheader("Metrics")
st.json(payload["metrics"])

probs = infer_probabilities(payload["model"], X)
th = st.slider("Alert Threshold (churn probability ≥)", 0.10, 0.90, 0.65, 0.05)
at_risk = probs[probs["churn_probability"] >= th]

st.subheader("Top At-Risk Customers")
st.dataframe(at_risk.head(50), use_container_width=True)
st.caption(f"{len(at_risk)} customers ≥ threshold {th:.2f}")

from src.utils.emailer import send_email

st.markdown("---")
st.subheader("🔔 Alerts")
to = st.text_input("Send alert to (email)")
if st.button("Send alerts for above at-risk list"):
    if not to:
        st.error("Enter an email address")
    else:
        body = "At-risk customers (top 20):\n" + "\n".join(
            f"{r.customer_id} — {r.churn_probability:.2f}" for _, r in at_risk.head(20).iterrows()
        )
        ok = send_email(to, "Churn Risk Alerts", body)
        st.success("Email sent." if ok else "SMTP not configured.")
