import streamlit as st
import pandas as pd
from src.data_processing.schema import normalize_columns, validate_schema

st.header("📁 Upload Data")
st.caption("CSV with columns: customer_id, purchase_date, transaction_amount (optional: product_id, region)")

use_sample = st.toggle("Load included sample data", value=True)

def show_validation_report(missing, extras, errors):
    if missing:
        st.error(f"Missing required columns: {missing}")
    if extras:
        st.info(f"Extra columns ignored/supported optionally: {extras}")
    if errors:
        st.warning("Type/parse issues:\n- " + "\n- ".join(errors))

df = None
if use_sample:
    df = pd.read_csv("assets/sample/customers.csv")

uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)

if df is not None:
    df = normalize_columns(df)
    df, missing, extras, errors = validate_schema(df)
    show_validation_report(missing, extras, errors)
    if missing:
        st.stop()
    st.session_state["data"] = df
    st.success(f"Loaded {len(df):,} rows.", icon="✅")
    st.subheader("Preview")
    st.dataframe(df.head(20), use_container_width=True)
