"""
validate_kpis.py
Independent check of the Power BI dashboard KPIs (success criterion SC1).

This script recalculates every headline KPI straight from the RAW CSV files in
data/raw/. It deliberately does NOT use data/processed/ or prepare_data.py, so
it is a separate path to the same numbers. Compare its output with the
dashboard; every value must match.

Run from the project root:   python src/validate_kpis.py
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"

# Only the columns needed are read, so no personal data is loaded.
enc = pd.read_csv(RAW / "encounters.csv",
                  usecols=["Id", "START", "STOP", "PAYER", "ENCOUNTERCLASS",
                           "TOTAL_CLAIM_COST", "PAYER_COVERAGE"])
proc = pd.read_csv(RAW / "procedures.csv", usecols=["ENCOUNTER"])

start = pd.to_datetime(enc["START"], utc=True)
stop = pd.to_datetime(enc["STOP"], utc=True)
hours = (stop - start).dt.total_seconds() / 3600
valid = (hours >= 0) & (hours <= 24 * 365)          # rule D1

results = {
    "Total Encounters": len(enc),
    "Total Procedures": len(proc),
    "Encounters With Procedures": proc["ENCOUNTER"].nunique(),
    "Total Claim Cost": round(enc["TOTAL_CLAIM_COST"].sum(), 2),
    "Total Payer Coverage": round(enc["PAYER_COVERAGE"].sum(), 2),
    "Average Claim Cost": round(enc["TOTAL_CLAIM_COST"].mean(), 2),
    "Median Claim Cost": round(enc["TOTAL_CLAIM_COST"].median(), 2),
    "Zero Coverage Encounters": int((enc["PAYER_COVERAGE"] == 0).sum()),
    "Zero Coverage %": f"{(enc['PAYER_COVERAGE'] == 0).mean() * 100:.2f}%",
    "Coverage Rate": f"{enc['PAYER_COVERAGE'].sum() / enc['TOTAL_CLAIM_COST'].sum() * 100:.2f}%",
    "Valid Duration Encounters": int(valid.sum()),
    "Over 24h Encounters": int(((hours > 24) & valid).sum()),
    "Over 24h %": f"{((hours > 24) & valid).sum() / valid.sum() * 100:.2f}%",
}

print("Independent KPI check (calculated from raw CSV files)\n")
width = max(len(k) for k in results)
for name, value in results.items():
    shown = f"{value:,}" if isinstance(value, (int, float)) else value
    print(f"{name:<{width}}  {shown:>18}")

print("\nEncounters by year")
for year, n in start.dt.year.value_counts().sort_index().items():
    print(f"  {year}: {n:,}")

print("\nEncounters by class")
for cls, n in enc["ENCOUNTERCLASS"].value_counts().items():
    print(f"  {cls:<12} {n:>8,}")