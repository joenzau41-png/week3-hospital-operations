# Data Quality Assessment

**Project:** Hospital Operations, Cost & Patient Flow Intelligence
**Programme:** AnalystLab Africa Experience Lab, Week 3
**Author:** NZAU
**Status:** Version 1.0, based on the supplied dataset pack

---

## 1. Purpose

This document records what was found when the supplied healthcare datasets were inspected **before** any analysis. It lists the tables and fields to be used, the size of each file, the quality issues found, the relationships between tables, and the limitations that could affect the validity of the work.

No records were deleted and no missing values were filled in while producing this assessment. Every cleaning decision is listed separately in Section 8 with its reason.

## 2. Files inspected

| File | Rows | Columns | Role in the project |
|---|---:|---:|---|
| `encounters.csv` | 27,891 | 14 | Main fact table: volumes, classes, duration, costs, payer coverage |
| `patients.csv` | 974 | 20 | Patient-level context (demographic fields only) |
| `procedures.csv` | 47,701 | 9 | Procedure frequency, base cost, utilisation |
| `payers.csv` | 10 | 7 | Payer names for payer-level analysis |
| `organizations.csv` | 1 | 8 | Identifies the single organisation in the data |
| `data_dictionary.csv` | 65 | 3 | Field definitions |

**Fields intended for use**

- `encounters`: Id, START, STOP, PATIENT, ORGANIZATION, PAYER, ENCOUNTERCLASS, CODE, DESCRIPTION, BASE_ENCOUNTER_COST, TOTAL_CLAIM_COST, PAYER_COVERAGE
- `procedures`: ENCOUNTER, PATIENT, CODE, DESCRIPTION, BASE_COST, START, STOP
- `payers`: Id, NAME
- `patients`: Id, BIRTHDATE, DEATHDATE, GENDER, RACE, ETHNICITY (used only if a patient-level question needs them)
- `organizations`: Id, NAME

**Fields deliberately not used (privacy):** patient name fields (PREFIX, FIRST, LAST, SUFFIX, MAIDEN), ADDRESS, CITY, ZIP, LAT, LON, BIRTHPLACE. These are dropped when the data is loaded and never appear in outputs.

## 3. Summary of results

| Check | Result |
|---|---|
| Duplicate rows (all tables) | None found |
| Duplicate primary keys | None found |
| Unparseable dates | None found |
| Encounters where STOP is before START | 0 |
| Negative cost values | 0 |
| Orphan keys (broken relationships) | 0 |
| Dictionary fields missing from CSVs | 2 (patients: `Middle`, `FIPS County Code`) |

The issues that need attention are listed in Section 5.

## 4. Missing values

| Table | Column | Missing | Share | Meaning |
|---|---|---:|---:|---|
| encounters | REASONCODE | 19,541 | 70.1% | No reason recorded for the visit. Left blank. |
| encounters | REASONDESCRIPTION | 19,541 | 70.1% | Same rows as REASONCODE |
| procedures | REASONCODE | 36,945 | 77.4% | No reason recorded. Left blank. |
| procedures | REASONDESCRIPTION | 36,945 | 77.4% | Same rows as REASONCODE |
| patients | DEATHDATE | 820 | 84.2% | Patient not recorded as deceased. Blank is meaningful. |
| patients | ZIP | 142 | 14.6% | Not used in this project |
| payers | ADDRESS, CITY, STATE_HEADQUARTERED, ZIP, PHONE | 1 row each | 10% | One payer row has no contact details. Not used. |

All cost, date, key and class columns in `encounters` have zero missing values.

**Treatment:** none of these blanks is imputed. Blank reason fields mean "no reason recorded", and blank DEATHDATE means "not deceased". Filling them would invent information.

## 5. Issues that affect the analysis

### 5.1 Extreme encounter durations
- Duration is `STOP - START`. Median is 0.25 hours (15 minutes), and 75% of encounters last under about 52 minutes.
- 75 encounters (0.27%) last more than 24 hours. By class: inpatient 58, outpatient 7, emergency 5, ambulatory 5.
- 4 encounters last **more than one year** (ambulatory 3, outpatient 1). The longest is about 5 years. These are not plausible for outpatient-type visits and look like data errors.
- **Effect:** the mean duration is distorted by these 4 rows (mean about 7.3 hours against a median of 0.25).
- **Treatment:** see Decision D1.

### 5.2 Incomplete first and last years
- Encounters run from 2 Jan 2011 to 5 Feb 2022.
- 2022 contains only 220 encounters because the data ends in early February.
- **Effect:** a year-over-year chart would show a false collapse in 2022.
- **Treatment:** see Decision D2.

| Year | Encounters |
|---|---:|
| 2011 | 1,336 |
| 2012 | 2,106 |
| 2013 | 2,495 |
| 2014 | 3,885 |
| 2015 | 2,469 |
| 2016 | 2,451 |
| 2017 | 2,360 |
| 2018 | 2,292 |
| 2019 | 2,228 |
| 2020 | 2,519 |
| 2021 | 3,530 |
| 2022 (to 5 Feb) | 220 |

### 5.3 Zero payer coverage is ambiguous
- 13,586 encounters (48.7%) have `PAYER_COVERAGE = 0`.
- All 8,807 encounters with payer `NO_INSURANCE` have zero coverage, which is expected.
- 4,779 of the 19,084 encounters with a named insurer (25.0%) **also** have zero coverage.
- **Effect:** "zero coverage" cannot be read as "uninsured". For insured patients it could mean a denied claim, an unpaid claim, a patient-paid service, or missing data. The dataset does not say which.
- **Treatment:** see Decision D4. The dashboard must label this metric as "zero **recorded** payer coverage".
- PAYER_COVERAGE never exceeds TOTAL_CLAIM_COST (0 violations).

### 5.4 Claim costs are highly skewed
| Column | Min | Median | Mean | Max |
|---|---:|---:|---:|---:|
| BASE_ENCOUNTER_COST | 85.55 | 136.80 | 116.18 | 146.18 |
| TOTAL_CLAIM_COST | 0.00 | 278.58 | 3,639.68 | 641,882.70 |
| PAYER_COVERAGE | 0.00 | 28.44 | 1,114.97 | 247,751.42 |

- The mean total claim cost is more than 13 times the median, so a few very expensive encounters dominate it.
- **Effect:** averages alone are misleading. Median and total should be shown alongside the mean.
- Currency is not stated in the data dictionary. Values are reported as recorded, without a currency symbol.

### 5.5 Zero total claim cost
- 89 encounters have `TOTAL_CLAIM_COST = 0`: wellness 51, inpatient 28, emergency 6, ambulatory 4.
- **Effect:** they lower average costs. It is unknown whether zero means "no charge" or "cost not recorded".
- **Treatment:** see Decision D3.

### 5.6 Procedure code and description inconsistencies
- 157 distinct procedure codes map to 163 distinct descriptions.
- 4 codes have more than one description. For example, code 171207006 appears as both "Depression screening" and "Depression screening (procedure)".
- 105 procedure descriptions have more than one `BASE_COST` value, so one procedure does not have a single fixed cost.
- **Effect:** counting by description can split one procedure into two. Ranking procedures by average base cost can be dominated by rare, expensive procedures.
- **Treatment:** see Decision D5.

### 5.7 Data dictionary mismatch
- The dictionary lists `Middle` and `FIPS County Code` for `patients`, but neither column exists in `patients.csv`.
- All fields in the other four tables match their CSVs exactly.
- **Treatment:** neither field is needed. The mismatch is recorded here and no analysis depends on them.

## 6. Relationships between tables

| Relationship | Check | Result |
|---|---|---|
| encounters.PATIENT → patients.Id | Unmatched rows | 0 |
| encounters.PAYER → payers.Id | Unmatched rows | 0 |
| encounters.ORGANIZATION → organizations.Id | Unmatched rows | 0 |
| procedures.ENCOUNTER → encounters.Id | Unmatched rows | 0 |
| procedures.PATIENT → patients.Id | Unmatched rows | 0 |
| patients with no encounter | Count | 0 |
| encounters with no procedure | Count | 13,221 (47.4%) |

**Cardinality**
- One patient has many encounters.
- One encounter has zero or many procedures.
- One payer has many encounters.
- All encounters belong to one organisation.

Because 47.4% of encounters have no procedure, procedure data must be joined with a left join from encounters. An inner join would silently remove nearly half of all encounters.

## 7. Encounter class distribution

| Class | Encounters |
|---|---:|
| ambulatory | 12,537 |
| outpatient | 6,300 |
| urgentcare | 3,666 |
| emergency | 2,322 |
| wellness | 1,931 |
| inpatient | 1,135 |

## 8. Decision log

| ID | Issue | Decision | Reason | Status |
|---|---|---|---|---|
| D1 | 4 encounters lasting more than 1 year | Exclude them from **duration calculations only**. Keep them in volume, cost, payer and procedure analysis. Flag them with a column such as `duration_valid`. | Their durations are implausible, but their cost, class and payer fields appear valid. | Confirmed |
| D2 | 2022 has data only to 5 Feb | Keep the rows. Label 2022 as "partial year" in trend charts and use full years for comparisons. | Deleting would lose real records. Leaving it unlabelled would mislead. | Proposed |
| D3 | 89 encounters with zero total claim cost | Keep them. Report them as a separate count and note their effect on averages. | Meaning of zero is unknown, so removal would be a guess. | Proposed |
| D4 | Zero payer coverage | Keep as recorded. Name the metric "zero recorded payer coverage" and report insured and uninsured zeros separately. | The data cannot distinguish unpaid, denied or missing. | Proposed |
| D5 | Procedure code and description mismatch | Count and group procedures by `CODE`. Use a single chosen description per code for display. For cost, show average base cost together with frequency. | Prevents split counts and one-off expensive procedures dominating a ranking. | Proposed |
| D6 | Skewed costs | Report median and total alongside the mean. | A few extreme claims distort the mean. | Proposed |
| D7 | Personal identifiers | Drop name, address and location columns at load. Never publish raw data. | Privacy requirement in the assignment brief. | Confirmed |
| D8 | Blank reason fields and DEATHDATE | Leave blank. No imputation. | Blank carries meaning. | Confirmed |

## 9. Limitations

1. **Single organisation.** All encounters come from one hospital, so findings cannot be generalised to other hospitals.
2. **Provenance not stated.** The brief does not say whether the data is real or simulated, and some patterns (for example, very regular base encounter costs) are worth noting. Findings describe this dataset only and should not be read as real hospital performance.
3. **No clinical outcomes.** The data holds no outcome measures, readmission flags or quality indicators. No clinical claims will be made.
4. **Cost meaning is limited.** The dictionary does not say who bears the cost beyond `PAYER_COVERAGE`, nor the currency.
5. **Repeat visits.** Patients appear many times. Treating encounters as independent observations can overstate statistical certainty in later hypothesis tests.
6. **Partial first and last years** affect trend interpretation (Section 5.2).

## 10. Reproducibility

All figures in this document come from reading the six supplied CSV files with Python and pandas, with no rows removed. The inspection code will be saved in `notebooks/` so that another analyst can regenerate every number above.
