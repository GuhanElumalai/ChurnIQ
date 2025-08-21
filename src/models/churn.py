import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.linear_model import LogisticRegression

def build_features(df: pd.DataFrame):
    d = df.copy()
    d["purchase_date"] = pd.to_datetime(d["purchase_date"])
    grp = d.groupby("customer_id").agg(
        total_spent=("transaction_amount","sum"),
        orders=("transaction_amount","count"),
        last_date=("purchase_date","max"),
        first_date=("purchase_date","min")
    ).reset_index()
    grp["avg_order_value"] = grp["total_spent"] / grp["orders"].clip(lower=1)
    grp["lifetime_days"] = (grp["last_date"] - grp["first_date"]).dt.days.clip(lower=1)
    grp["order_rate_monthly"] = grp["orders"] / (grp["lifetime_days"]/30.0)
    # Create synthetic churn label (demo): low activity + old recency -> higher churn
    recency_days = (d["purchase_date"].max() - grp["last_date"]).dt.days
    churn_score = 0.4*(recency_days/recency_days.max()) + 0.6*(1 - grp["order_rate_monthly"]/grp["order_rate_monthly"].max())
    y = (churn_score > churn_score.median()).astype(int)  # 1 means churned
    X = grp[["total_spent","orders","avg_order_value","order_rate_monthly"]].fillna(0)
    X.index = grp["customer_id"]
    return X, y

def train_baseline(X, y):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = LogisticRegression(max_iter=1000)
    model.fit(Xtr, ytr)
    p = model.predict_proba(Xte)[:,1]
    metrics = {
        "auc": float(roc_auc_score(yte, p)),
        "accuracy": float(accuracy_score(yte, (p>0.5).astype(int)))
    }
    return model, metrics

def infer_probabilities(model, X):
    p = model.predict_proba(X)[:,1]
    out = pd.DataFrame({"customer_id": X.index, "churn_probability": p})
    return out.sort_values("churn_probability", ascending=False).reset_index(drop=True)
