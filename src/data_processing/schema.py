# src/data_processing/schema.py
import pandas as pd

REQUIRED = ["customer_id", "purchase_date", "transaction_amount"]
OPTIONAL = ["product_id", "region"]

ALIASES = {
    "customer_id": {"customer_id","customer id","cust_id","cid","id"},
    "purchase_date": {"purchase_date","purchase date","date","order_date","order date"},
    "transaction_amount": {"transaction_amount","amount","price","value","revenue","sales"},
    "product_id": {"product_id","product id","sku","item_id"},
    "region": {"region","state","area","district"}
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # strip/lower/snake
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    # alias mapping
    colmap = {}
    for canonical, synonyms in ALIASES.items():
        for c in list(df.columns):
            if c in synonyms:
                colmap[c] = canonical
    df = df.rename(columns=colmap)
    return df

def validate_schema(df: pd.DataFrame):
    cols = set(df.columns)
    missing = [c for c in REQUIRED if c not in cols]
    extras = [c for c in df.columns if c not in REQUIRED + OPTIONAL]
    # Type coercions
    errors = []
    out = df.copy()
    if "purchase_date" in out.columns:
        try:
            out["purchase_date"] = pd.to_datetime(out["purchase_date"])
        except Exception:
            errors.append("purchase_date: cannot parse to datetime")
    if "transaction_amount" in out.columns:
        try:
            out["transaction_amount"] = pd.to_numeric(out["transaction_amount"], errors="coerce")
        except Exception:
            errors.append("transaction_amount: cannot convert to numeric")
    if "customer_id" in out.columns:
        out["customer_id"] = out["customer_id"].astype(str).str.strip()

    return out, missing, extras, errors
