"""Pandas-based summaries and aggregation for recorded expenses."""
import pandas as pd

def expense_frame(expenses):
    df=pd.DataFrame(expenses)
    if df.empty: return pd.DataFrame(columns=["id","title","amount","category","expense_date","notes"])
    df["amount"]=pd.to_numeric(df["amount"],errors="coerce")
    df["expense_date"]=pd.to_datetime(df["expense_date"],errors="coerce")
    return df.dropna(subset=["amount","expense_date"])

def monthly_totals(expenses, fill_gaps=True):
    df=expense_frame(expenses)
    if df.empty: return pd.Series(dtype=float, name="amount")
    totals=df.set_index("expense_date").resample("MS")["amount"].sum().astype(float)
    if fill_gaps:
        totals=totals.reindex(pd.date_range(totals.index.min(),totals.index.max(),freq="MS"),fill_value=0.0)
    totals.name="amount"
    return totals
