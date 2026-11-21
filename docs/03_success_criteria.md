# Success Criteria

**Project:** Hospital Operations, Cost & Patient Flow Intelligence
**Programme:** AnalystLab Africa Experience Lab, Week 3
**Author:** NZAU
**Related documents:** [01_data_quality_assessment.md](01_data_quality_assessment.md), [02_problem_statement.md](02_problem_statement.md)

---

## 1. Purpose

These criteria define, **before the work is built**, how we will decide whether the dashboard is correct and useful. Each one is measurable, has a clear pass condition, and says what evidence will be saved.

The "Result" column is left empty on purpose. It is filled in during validation, with real evidence.

## 2. Criteria

### SC1. Dashboard numbers reconcile with an independent calculation

| Item | Detail |
|---|---|
| **What is checked** | At least three key dashboard figures are recomputed independently in SQL or Python straight from the raw CSV files |
| **Figures to check** | (a) total number of encounters, (b) total claim cost, (c) number of encounters with zero recorded payer coverage. Further checks: share of encounters over 24 hours, and the most frequent procedure |
| **Pass condition** | Dashboard value and independent value are **identical** for counts, and agree to within 0.01 for monetary totals (rounding only) |
| **If it fails** | Investigate and document the cause (for example a filter, a join, or a duration rule) before the dashboard is accepted |
| **Evidence saved** | Validation table with dashboard value, independent value, difference, and the query or code used (`docs/validation_evidence.md`) |

### SC2. Dashboard totals respond correctly to filters

| Item | Detail |
|---|---|
| **What is checked** | After applying slicers (year, encounter class, payer), the figures change correctly |
| **Tests** | (a) Select one encounter class: the total encounters shown equals that class's count from the source data. (b) Select one payer: encounter count and total claim cost match the source. (c) With no filter, the sum of all encounter classes equals the overall total. (d) The sum of encounters across all years equals the overall total |
| **Pass condition** | All four tests give matching values with no unexplained difference |
| **If it fails** | Check relationships between tables and filter direction in the data model |
| **Evidence saved** | Screenshots of each filtered view next to the source-data count |

### SC3. Every KPI has a reproducible written definition

| Item | Detail |
|---|---|
| **What is checked** | A KPI definition sheet exists, and each KPI can be recalculated by another analyst using only that sheet |
| **Each definition contains** | KPI name, business meaning, source table and field, exact calculation (formula or DAX), filters or exclusions (for example the duration rule), and a known limitation |
| **Targets** | At least **five** KPIs defined. The same sheet covers every KPI shown on the dashboard |
| **Pass condition** | No KPI on the dashboard is missing from the sheet, and at least one KPI is recalculated by following only the written definition and gives the dashboard value |
| **Evidence saved** | `docs/kpi_definitions.md` plus the recalculation note |

## 3. Supporting quality checks

These are not scored on their own, but must be true for the criteria above to mean anything.

| Check | Pass condition |
|---|---|
| Data-quality issues documented | Every issue in `01_data_quality_assessment.md` has a recorded decision |
| Misleading metrics flagged | The dashboard labels zero recorded payer coverage, partial 2022 data and skewed averages |
| Privacy | No patient names, addresses or other identifiers appear in any chart, screenshot or file in the repository |
| Reproducibility | Someone can rerun the data preparation from the raw CSVs and obtain the same numbers |

## 4. Validation record (to be completed)

| Criterion | Test | Dashboard value | Independent value | Match? | Evidence file |
|---|---|---|---|---|---|
| SC1 | Total encounters | | | | |
| SC1 | Total claim cost | | | | |
| SC1 | Zero recorded coverage count | | | | |
| SC2 | Filter by one encounter class | | | | |
| SC2 | Filter by one payer | | | | |
| SC2 | Sum of classes equals total | | | | |
| SC2 | Sum of years equals total | | | | |
| SC3 | Recalculate one KPI from its definition | | | | |

## 5. Note on later tracks

If the statistical investigation (Track B) and the predictive model (Track C) are completed, they will have their own criteria, added to this file: for example, a documented test of assumptions for each hypothesis, and a model that beats a simple baseline on a stated metric.
