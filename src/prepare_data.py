"""
prepare_data.py
Hospital Operations, Cost & Patient Flow Intelligence (AnalystLab Africa, Week 3)

Reads the six raw CSV files from data/raw/ and writes clean, analysis-ready
tables to data/processed/. Raw files are never modified.

Rules applied (see docs/01_data_quality_assessment.md, Section 8):
  D1  Encounters longer than 1 year are flagged duration_valid = False.
      They are excluded from duration calculations only and kept everywhere else.
  D2  Encounters in the final partial year are flagged is_partial_year.
  D3  Zero total-claim-cost encounters are kept and flagged.
  D4  Zero payer coverage is kept as recorded and flagged (insured vs uninsured).
  D5  Procedures are grouped by CODE, using one standard description per code.
  D7  Name, address and location columns are never loaded.
  D8  Blank reason fields and blank dates are left blank (no imputation).

Run from the project root:   python src/prepare_data.py
"""
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"

MAX_PLAUSIBLE_HOURS = 24 * 365          # D1: longer than one year is implausible
NO_INSURANCE_NAME = "NO_INSURANCE"

# D7: only these patient columns are ever read. Names, addresses and
# coordinates are deliberately left out.
PATIENT_COLS = ["Id", "BIRTHDATE", "DEATHDATE", "GENDER", "RACE", "ETHNICITY"]


def read_raw():
    enc = pd.read_csv(RAW / "encounters.csv")
    pat = pd.read_csv(RAW / "patients.csv", usecols=PATIENT_COLS)
    proc = pd.read_csv(RAW / "procedures.csv")
    pay = pd.read_csv(RAW / "payers.csv", usecols=["Id", "NAME"])
    org = pd.read_csv(RAW / "organizations.csv", usecols=["Id", "NAME"])
    return enc, pat, proc, pay, org


def build_encounters(enc, pay):
    df = enc.copy()
    df["start_ts"] = pd.to_datetime(df["START"], utc=True)
    df["stop_ts"] = pd.to_datetime(df["STOP"], utc=True)

    # Duration (hours) and the D1 validity flag. Duration is never blanked:
    # we keep the raw value and only mark it as unreliable.
    df["duration_hours"] = (df["stop_ts"] - df["start_ts"]).dt.total_seconds() / 3600
    df["duration_valid"] = (df["duration_hours"] >= 0) & (df["duration_hours"] <= MAX_PLAUSIBLE_HOURS)
    # Over-24h flag is only defined where the duration is valid.
    df["over_24h"] = (df["duration_hours"] > 24) & df["duration_valid"]

    # Calendar fields for trend analysis
    df["start_date"] = df["start_ts"].dt.date
    df["year"] = df["start_ts"].dt.year
    df["quarter"] = df["start_ts"].dt.quarter
    df["year_month"] = df["start_ts"].dt.strftime("%Y-%m")
    last_year = df["year"].max()
    df["is_partial_year"] = df["year"] == last_year           # D2 (data stops early in last year)

    # Payer name and insured flag
    names = pay.set_index("Id")["NAME"]
    df["payer_name"] = df["PAYER"].map(names)
    df["is_insured"] = df["payer_name"] != NO_INSURANCE_NAME

    # Cost flags (D3, D4)
    df["zero_total_claim"] = df["TOTAL_CLAIM_COST"] == 0
    df["zero_recorded_coverage"] = df["PAYER_COVERAGE"] == 0
    df["uncovered_amount"] = (df["TOTAL_CLAIM_COST"] - df["PAYER_COVERAGE"]).round(2)

    # Power BI-friendly timestamps (no timezone suffix)
    df["start_ts"] = df["start_ts"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["stop_ts"] = df["stop_ts"].dt.strftime("%Y-%m-%d %H:%M:%S")

    out = df.rename(columns={
        "Id": "encounter_id", "PATIENT": "patient_id", "ORGANIZATION": "organization_id",
        "PAYER": "payer_id", "ENCOUNTERCLASS": "encounter_class", "CODE": "encounter_code",
        "DESCRIPTION": "encounter_description", "BASE_ENCOUNTER_COST": "base_encounter_cost",
        "TOTAL_CLAIM_COST": "total_claim_cost", "PAYER_COVERAGE": "payer_coverage",
        "REASONCODE": "reason_code", "REASONDESCRIPTION": "reason_description",
    })
    cols = ["encounter_id", "start_ts", "stop_ts", "start_date", "year", "quarter", "year_month",
            "is_partial_year", "patient_id", "organization_id", "payer_id", "payer_name", "is_insured",
            "encounter_class", "encounter_code", "encounter_description",
            "base_encounter_cost", "total_claim_cost", "payer_coverage", "uncovered_amount",
            "zero_total_claim", "zero_recorded_coverage",
            "duration_hours", "duration_valid", "over_24h",
            "reason_code", "reason_description"]
    return out[cols]


def build_patients(pat):
    df = pat.copy()
    # Birth year instead of full birth date (less identifying). D7.
    df["birth_year"] = pd.to_datetime(df["BIRTHDATE"], errors="coerce").dt.year
    df["is_deceased"] = df["DEATHDATE"].notna()               # D8: blank = not deceased
    out = df.rename(columns={"Id": "patient_id", "GENDER": "gender",
                             "RACE": "race", "ETHNICITY": "ethnicity"})
    return out[["patient_id", "birth_year", "gender", "race", "ethnicity", "is_deceased"]]


def build_procedures(proc):
    df = proc.copy()
    # D5: one standard description per code = the most frequent wording for that code.
    std = (df.groupby("CODE")["DESCRIPTION"]
             .agg(lambda s: s.value_counts().idxmax())
             .rename("procedure_description"))
    df = df.join(std, on="CODE")
    out = df.rename(columns={"ENCOUNTER": "encounter_id", "PATIENT": "patient_id",
                             "CODE": "procedure_code", "DESCRIPTION": "procedure_description_raw",
                             "BASE_COST": "base_cost", "REASONCODE": "reason_code",
                             "REASONDESCRIPTION": "reason_description"})
    out["start_ts"] = pd.to_datetime(out["START"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")
    out["stop_ts"] = pd.to_datetime(out["STOP"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")
    cols = ["encounter_id", "patient_id", "procedure_code", "procedure_description",
            "procedure_description_raw", "base_cost", "start_ts", "stop_ts",
            "reason_code", "reason_description"]
    return out[cols]


def build_payers(pay):
    out = pay.rename(columns={"Id": "payer_id", "NAME": "payer_name"}).copy()
    out["is_insured"] = out["payer_name"] != NO_INSURANCE_NAME
    return out


def build_organizations(org):
    return org.rename(columns={"Id": "organization_id", "NAME": "organization_name"})


def validate(raw, tables):
    """Basic checks so a silent mistake cannot slip through."""
    enc, pat, proc, pay, org = raw
    problems = []

    # Row counts must be unchanged: we flag, we do not delete.
    if len(tables["fact_encounters"]) != len(enc):
        problems.append("encounter row count changed")
    if len(tables["fact_procedures"]) != len(proc):
        problems.append("procedure row count changed")
    if len(tables["dim_patients"]) != len(pat):
        problems.append("patient row count changed")

    # Keys must still be unique and links must still work.
    if tables["fact_encounters"]["encounter_id"].duplicated().any():
        problems.append("duplicate encounter_id")
    if not tables["fact_encounters"]["patient_id"].isin(tables["dim_patients"]["patient_id"]).all():
        problems.append("encounters with unknown patient")
    if not tables["fact_encounters"]["payer_id"].isin(tables["dim_payers"]["payer_id"]).all():
        problems.append("encounters with unknown payer")
    if not tables["fact_procedures"]["encounter_id"].isin(tables["fact_encounters"]["encounter_id"]).all():
        problems.append("procedures with unknown encounter")

    # Privacy: no name/address columns may appear in any output.
    banned = {"FIRST", "LAST", "PREFIX", "SUFFIX", "MAIDEN", "ADDRESS", "CITY", "ZIP",
              "LAT", "LON", "BIRTHPLACE", "BIRTHDATE", "DEATHDATE"}
    for name, t in tables.items():
        leaked = banned.intersection({c.upper() for c in t.columns})
        if leaked:
            problems.append(f"{name} contains personal columns: {sorted(leaked)}")

    # Money must be preserved exactly.
    if round(tables["fact_encounters"]["total_claim_cost"].sum(), 2) != round(enc["TOTAL_CLAIM_COST"].sum(), 2):
        problems.append("total claim cost changed")
    return problems


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    raw = read_raw()
    enc, pat, proc, pay, org = raw

    tables = {
        "fact_encounters": build_encounters(enc, pay),
        "fact_procedures": build_procedures(proc),
        "dim_patients": build_patients(pat),
        "dim_payers": build_payers(pay),
        "dim_organizations": build_organizations(org),
    }

    problems = validate(raw, tables)
    if problems:
        print("VALIDATION FAILED:")
        for p in problems:
            print(" -", p)
        sys.exit(1)

    for name, t in tables.items():
        t.to_csv(OUT / f"{name}.csv", index=False)

    e = tables["fact_encounters"]
    print("Data preparation complete. All validation checks passed.\n")
    print(f"{'table':<20}{'rows':>10}{'columns':>10}")
    for name, t in tables.items():
        print(f"{name:<20}{len(t):>10,}{t.shape[1]:>10}")
    print("\nFlag summary (fact_encounters)")
    print(f"  duration_valid = False : {(~e['duration_valid']).sum():,}")
    print(f"  over_24h               : {e['over_24h'].sum():,}")
    print(f"  is_partial_year        : {e['is_partial_year'].sum():,}")
    print(f"  zero_total_claim       : {e['zero_total_claim'].sum():,}")
    print(f"  zero_recorded_coverage : {e['zero_recorded_coverage'].sum():,}")
    print(f"\nFiles written to: {OUT}")


if __name__ == "__main__":
    main()