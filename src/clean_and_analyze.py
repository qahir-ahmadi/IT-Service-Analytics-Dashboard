from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw" / "it_tickets_raw.csv"
OUT = BASE / "data" / "processed" / "it_tickets_clean.csv"
KPI = BASE / "data" / "processed" / "monthly_kpis.csv"

df = pd.read_csv(RAW, parse_dates=["opened_date", "resolved_date"])
df = df.drop_duplicates(subset=["ticket_id"]).copy()

for col in ["department", "location", "category", "priority", "technician", "status", "issue_summary"]:
    df[col] = df[col].astype(str).str.strip()

df["opened_month"] = df["opened_date"].dt.to_period("M").astype(str)
df["is_closed"] = df["status"].isin(["Closed", "Resolved"])
df["is_backlog"] = ~df["is_closed"]
df["sla_met_flag"] = df["sla_met"].map({True: 1, False: 0})

df.to_csv(OUT, index=False)

closed = df[df["is_closed"]].copy()
monthly = (
    closed.groupby("opened_month")
    .agg(
        tickets_closed=("ticket_id", "count"),
        avg_resolution_hours=("resolution_hours", "mean"),
        avg_satisfaction=("satisfaction_score", "mean"),
        sla_compliance=("sla_met_flag", "mean"),
    )
    .reset_index()
)

monthly["sla_compliance"] = (monthly["sla_compliance"] * 100).round(2)
monthly["avg_resolution_hours"] = monthly["avg_resolution_hours"].round(2)
monthly["avg_satisfaction"] = monthly["avg_satisfaction"].round(2)
monthly.to_csv(KPI, index=False)

print(f"Saved: {OUT}")
print(f"Saved: {KPI}")
