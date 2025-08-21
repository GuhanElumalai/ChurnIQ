import pandas as pd

def aggregate_daily_sales(df: pd.DataFrame, date_col="purchase_date", amount_col="transaction_amount"):
    d = df.copy()
    d[date_col] = pd.to_datetime(d[date_col])
    daily = d.groupby(d[date_col].dt.date)[amount_col].sum().rename("sales").to_frame()
    daily.index = pd.to_datetime(daily.index)
    daily = daily.asfreq("D").fillna(0)
    return daily["sales"]

def rolling_forecast(series: pd.Series, window=7, horizon=30):
    hist = series.copy()
    ma = hist.rolling(window=window, min_periods=1).mean()
    last = ma.iloc[-1] if len(ma) else 0
    # Flat forecast at last rolling mean
    future_index = pd.date_range(hist.index[-1] + pd.Timedelta(days=1), periods=horizon, freq="D")
    forecast = pd.Series([float(last)]*horizon, index=future_index, name="forecast")
    return hist, forecast
