# KPI Definition Sheet

**Project:** Hospital Operations, Cost & Patient Flow Intelligence
**Programme:** AnalystLab Africa Experience Lab, Week 3
**Author:** Joel nzau
**Dashboard file:** `hospital_operations.pbix` (Power BI Desktop)
**Related documents:** [01_data_quality_assessment.md](01_data_quality_assessment.md), [03_success_criteria.md](03_success_criteria.md)

---

## 1. Purpose

This sheet defines every KPI shown on the dashboard so that another analyst can rebuild and check each one. For each KPI it gives the business meaning, the source field, the exact DAX calculation, the value when no filter is applied, and the page where it appears.

This sheet meets success criterion **SC3**.

## 2. Data model

| Table | Role | Key |
|---|---|---|
| `fact_encounters` | One row per encounter (27,891 rows) | `encounter_id` |
| `fact_procedures` | One row per procedure (47,701 rows) | links by `encounter_id` |
| `dim_patients` | Patient attributes without names or addresses | `patient_id` |
| `dim_payers` | Payer names | `payer_id` |
| `dim_organizations` | The single organisation | `organization_id` |
| `dim_date` | Calendar table, 2011 to 2022 | `Date` |

**Relationships (all one-to-many, single direction):**
`dim_patients[patient_id]` to `fact_encounters[patient_id]`, `dim_payers[payer_id]` to `fact_encounters[payer_id]`, `dim_organizations[organization_id]` to `fact_encounters[organization_id]`, `dim_date[Date]` to `fact_encounters[start_date]`, and `fact_encounters[encounter_id]` to `fact_procedures[encounter_id]`.

**Slicers (synced across pages):** Year (`dim_date[Year]`), Encounter class (`fact_encounters[encounter_class]`), Payer (`dim_payers[payer_name]`).

**Source of the tables:** produced from the raw CSV files by `src/prepare_data.py`. Raw files are never edited.

## 3. Volume KPIs

| KPI | Business meaning | DAX | Value, no filter | Page |
|---|---|---|---:|---|
| Total Encounters | Number of recorded encounters | `COUNTROWS(fact_encounters)` | 27,891 | Overview, Operations, Finance |
| Total Procedures | Number of recorded procedures | `COUNTROWS(fact_procedures)` | 47,701 | Overview, Procedures |
| Encounters With Procedures | Encounters that have at least one procedure | `DISTINCTCOUNT(fact_procedures[encounter_id])` | 14,670 | Validation page |
| Distinct Procedure Codes | Number of different procedure codes | `DISTINCTCOUNT(fact_procedures[procedure_code])` | 157 | Procedures |

## 4. Cost KPIs

| KPI | Business meaning | DAX | Value, no filter | Page |
|---|---|---|---:|---|
| Total Claim Cost | Sum of recorded total claim cost | `SUM(fact_encounters[total_claim_cost])` | 101,514,375.52 | Overview, Finance |
| Average Claim Cost | Mean claim cost per encounter | `AVERAGE(fact_encounters[total_claim_cost])` | 3,639.68 | Finance (payer table) |
| Median Claim Cost | Middle claim cost per encounter | `MEDIAN(fact_encounters[total_claim_cost])` | 278.58 | Overview, Finance |
| Average Base Cost | Mean recorded base cost per procedure | `AVERAGE(fact_procedures[base_cost])` | 2,212.06 | Procedures |

## 5. Payer coverage KPIs

| KPI | Business meaning | DAX | Value, no filter | Page |
|---|---|---|---:|---|
| Total Payer Coverage | Sum of recorded payer coverage | `SUM(fact_encounters[payer_coverage])` | 31,097,506.99 | Finance |
| Coverage Rate | Recorded payer coverage as a share of total claim cost | `DIVIDE([Total Payer Coverage], [Total Claim Cost])` | 30.63% | Finance |
| Zero Coverage Encounters | Encounters where recorded payer coverage is 0 | `CALCULATE([Total Encounters], fact_encounters[zero_recorded_coverage] = TRUE())` | 13,586 | Finance |
| Zero Coverage % | Zero Coverage Encounters as a share of all encounters | `DIVIDE([Zero Coverage Encounters], [Total Encounters])` | 48.71% | Overview, Finance |

## 6. Duration KPIs

These apply decision D1: encounters lasting more than one year are treated as invalid durations and excluded from the duration KPIs only.

| KPI | Business meaning | DAX | Value, no filter | Page |
|---|---|---|---:|---|
| Valid Duration Encounters | Encounters with a plausible duration (0 to 365 days). Denominator for the over-24h share | `CALCULATE([Total Encounters], fact_encounters[duration_valid] = TRUE())` | 27,887 | Supporting measure |
| Over 24h Encounters | Valid-duration encounters lasting more than 24 hours | `CALCULATE([Total Encounters], fact_encounters[over_24h] = TRUE())` | 71 | Operations |
| Over 24h % | Over 24h Encounters as a share of valid-duration encounters | `DIVIDE([Over 24h Encounters], [Valid Duration Encounters])` | 0.25% | Overview |

## 7. Calculated columns used by the KPIs (created in `src/prepare_data.py`)

| Column | Definition |
|---|---|
| `duration_hours` | `STOP` minus `START`, in hours |
| `duration_valid` | True when `duration_hours` is between 0 and 8,760 (one year) |
| `over_24h` | True when `duration_hours` is greater than 24 and `duration_valid` is True |
| `zero_recorded_coverage` | True when `PAYER_COVERAGE` equals 0 |
| `zero_total_claim` | True when `TOTAL_CLAIM_COST` equals 0 |
| `is_partial_year` | True for encounters in the last year of the data (2022) |
| `is_insured` | True when the payer is not `NO_INSURANCE` |
| `procedure_description` | The most frequent wording recorded for each `procedure_code` (decision D5) |

## 8. Dashboard rules and filters

| Visual | Rule applied |
|---|---|
| Encounters per full year (Operations) | Filter `is_partial_year` = False, so 2022 (220 encounters, data ends 5 Feb) is excluded from the trend line only. It remains in all totals. |
| Ten most frequent procedures | Top 10 `procedure_description` by Total Procedures |
| Highest average base cost (Procedures) | Only procedures with Total Procedures of at least 100, so averages are not driven by a few cases |
| Payer table (Finance) | Shows Total Encounters beside average cost, so frequency is always visible |

## 9. Known limitations by KPI

| KPI | Limitation |
|---|---|
| Total / Average / Median Claim Cost | Currency is not stated in the data dictionary. Costs are very skewed (mean 3,639.68 against median 278.58), so averages should be read together with the median. 89 encounters have a claim cost of 0 and are kept. |
| Zero Coverage Encounters and %, Coverage Rate | Zero recorded coverage does not prove a claim was unpaid. For insured patients it could mean denied, unpaid, patient-paid or not recorded. 4,779 encounters with a named insurer have zero coverage. Label as "zero recorded payer coverage". |
| Over 24h Encounters and % | The 4 encounters lasting more than a year are excluded from the denominator, so it is 27,887, not 27,891. |
| Average Base Cost | The same procedure can have different base costs (105 procedure descriptions have more than one value). Base cost is a recorded base amount, not necessarily what was charged or paid. |
| Total Encounters by year | 2022 is a partial year. Trends should use 2011 to 2021 for full-year comparisons. |
| All KPIs | One organisation only, so findings do not generalise. No clinical outcome data, so no clinical claims are made. |

## 10. Reproduction test (SC3)

**Test:** recalculate **Over 24h %** using only the definitions above.

1. Read `encounters.csv`. Compute `duration_hours` = `STOP` minus `START`, in hours.
2. Mark a duration valid when it is between 0 and 8,760 hours. Count the valid ones: **27,887**.
3. Among the valid ones, count those with duration above 24 hours: **71**.
4. Divide: 71 / 27,887 = **0.25%**.

The script `src/validate_kpis.py` carries out exactly these steps from the raw files and prints the same value that the dashboard shows. All 13 KPI values it prints match the dashboard (see `docs/validation_independent_check.txt`).

| Check | Dashboard | Rebuilt from this sheet | Match |
|---|---:|---:|---|
| Over 24h Encounters | 71 | 71 | Yes |
| Valid Duration Encounters | 27,887 | 27,887 | Yes |
| Over 24h % | 0.25% | 0.25% | Yes |
