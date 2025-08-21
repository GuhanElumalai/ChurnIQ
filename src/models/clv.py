import pandas as pd
import numpy as np

def compute_rfm(df: pd.DataFrame, customer_col="customer_id", date_col="purchase_date", amount_col="transaction_amount"):
    d = df.copy()
    d[date_col] = pd.to_datetime(d[date_col])
    ref_date = d[date_col].max() + pd.Timedelta(days=1)
    g = d.groupby(customer_col)
    recency = (ref_date - g[date_col].max()).dt.days
    frequency = g[date_col].count()
    monetary = g[amount_col].sum()
    rfm = pd.DataFrame({"customer_id": recency.index, "recency": recency.values, "frequency": frequency.values, "monetary": monetary.values})
    rfm["avg_purchase_value"] = rfm["monetary"] / rfm["frequency"].replace(0, np.nan)
    rfm["purchase_frequency_monthly"] = rfm["frequency"] / max(((ref_date - d[date_col].min()).days / 30.0), 1)
    rfm = rfm.fillna(0)
    return rfm.sort_values("monetary", ascending=False)

def simple_clv(rfm: pd.DataFrame, margin_pct=0.6, months=12, retention_pct=0.85):
    out = rfm.copy()
    out["expected_gross_revenue_monthly"] = out["avg_purchase_value"].fillna(0) * out["purchase_frequency_monthly"]
    out["expected_gross_margin_monthly"] = out["expected_gross_revenue_monthly"] * margin_pct
    # Geometric retention over horizon
    retention_factor = (1 - (1 - retention_pct) ** months) / (1 - (1 - retention_pct) + 1e-9)
    out["clv_proxy"] = out["expected_gross_margin_monthly"] * retention_factor
    cols = ["customer_id","recency","frequency","monetary","avg_purchase_value","purchase_frequency_monthly","clv_proxy"]
    return out[cols].sort_values("clv_proxy", ascending=False).reset_index(drop=True)

def add_clv_segments(clv_df: pd.DataFrame):
    q = clv_df["clv_proxy"].quantile([0.8, 0.5]).to_list()
    top, mid = q[0], q[1]
    def tag(v):
        if v >= top: return "Platinum"
        if v >= mid: return "Gold"
        return "Silver"
    out = clv_df.copy()
    out["segment"] = out["clv_proxy"].apply(tag)
    return out
