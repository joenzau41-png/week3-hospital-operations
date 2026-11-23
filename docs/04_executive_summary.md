# Executive Summary

**Project:** Hospital Operations, Cost & Patient Flow Intelligence
**Programme:** AnalystLab Africa Experience Lab, Week 3 (Track A: Data Analytics)
**Author:** Joel nzau
**Audience:** Hospital operations manager and finance / revenue manager

---

## 1. What this work covers

An interactive Power BI dashboard built on the supplied encounter, procedure, patient and payer data for one hospital organisation, covering **2 January 2011 to 5 February 2022**. It has four pages (Overview, Operations, Finance, Procedures) with synced filters for year, encounter class and payer.

The dashboard describes what the data records. It does not make clinical claims and it does not prove causes.

## 2. Headline numbers

| Measure | Value |
|---|---:|
| Encounters | 27,891 |
| Procedures | 47,701 |
| Total claim cost | 101,514,375.52 |
| Median claim cost per encounter | 278.58 |
| Recorded payer coverage | 31,097,506.99 (30.63% of claim cost) |
| Encounters with zero recorded payer coverage | 13,586 (48.71%) |
| Encounters over 24 hours (valid durations) | 71 of 27,887 (0.25%) |

## 3. Key findings

**F1. Volume rose in two bursts, with a steady plateau between.**
Encounters grew from 1,336 in 2011 to a peak of 3,885 in 2014 (up 55.7% on 2013), settled between 2,228 and 2,519 a year from 2015 to 2020, then rose to 3,530 in 2021 (up 40.1% on 2020). 2022 holds only 220 encounters because the data stops on 5 February, so it is left out of the trend line.

**F2. Urgent care costs far more than its share of volume.**
Ambulatory is the largest class (44.9% of encounters, 35.7% of claim cost). Urgent care is 13.1% of encounters but 23.0% of claim cost, with an average claim of 6,369 against a median of only 142.58. Inpatient is 4.1% of encounters and 8.7% of cost, at an average of 7,761.

**F3. Long stays are rare and almost all inpatient.**
71 encounters lasted more than 24 hours. 58 of them (81.7%) are inpatient, which is 5.1% of all inpatient encounters. Their average claim cost is 29,068.22, about eight times the overall average of 3,639.68.

**F4. A small share of encounters carries a large share of cost.**
The mean claim (3,639.68) is more than thirteen times the median (278.58). The most expensive 1% of encounters (278) account for 14.5% of total claim cost, the top 5% for 44.6%, and the top 10% for 66.6%.

**F5. Zero recorded coverage is concentrated in five commercial payers.**
Medicare and Medicaid have almost no zero-coverage encounters (0.54% and 0.35%), and recorded coverage there equals 82.2% of their claim cost. In contrast, Anthem, Cigna, Aetna, Humana and UnitedHealthcare have 4,250 zero-coverage encounters out of 4,433 (95.9%). Those 4,250 encounters carry 13,746,319 of claim cost, which is 13.5% of the total.

**F6. Uninsured encounters hold almost half of all claim cost.**
Encounters recorded as `NO_INSURANCE` are 31.6% of encounters but 48.5% of claim cost (49,259,290). Their average claim is 5,593.20, against 2,738.16 for insured encounters. All of them show zero recorded coverage, as expected.

**F7. Procedure workload and procedure cost are different lists.**
The most frequent procedures are screenings and assessments (each between 2,288 and 4,596 procedures). The highest average base cost among procedures performed at least 100 times is electrical cardioversion (1,383 procedures at an average of 25,903.11), which alone accounts for about 34% of all recorded procedure base cost (35,824,002 of 105,517,711).

## 4. Recommendations

### R1. Establish why insured encounters show zero recorded coverage
| | |
|---|---|
| **Finding** | 4,779 encounters with a named insurer have zero recorded coverage. 4,250 of them belong to five commercial payers (F5), carrying 13.7 million of claim cost. |
| **Action** | Finance reviews a sample of these encounters to find out whether the claims were denied, unpaid, patient-paid or simply not recorded. Add a claim-status field to the data feed so the reason is captured in future. |
| **Benefit** | Turns the largest unexplained gap in the data into a known category, and shows whether there is recoverable revenue. |
| **Limitation** | The data cannot say why coverage is zero. No claim should be called unpaid until the sample is reviewed. |

### R2. Review billing and financial-assistance handling for uninsured encounters
| | |
|---|---|
| **Finding** | Uninsured encounters are 31.6% of volume and 48.5% of claim cost (F6). |
| **Action** | Finance reviews how these encounters are billed and what is later recovered, split by encounter class, starting with urgent care and ambulatory. |
| **Benefit** | Focuses attention on the single largest cost group. |
| **Limitation** | The dataset holds no patient payments, write-offs or charity care, so recovery cannot be measured from this data. |

### R3. Review urgent care cost drivers and staffing alongside volume
| | |
|---|---|
| **Finding** | Urgent care is 13.1% of encounters but 23.0% of claim cost, and its average claim is 45 times its median (F2). |
| **Action** | Operations and finance examine the small set of high-cost urgent care encounters and track urgent care cost per month as a standing indicator. |
| **Benefit** | Separates ordinary urgent care visits from a few costly ones, so planning is not based on a misleading average. |
| **Limitation** | There is no staffing, capacity or clinical detail in the data, so the reasons for high cost cannot be identified here. |

### R4. Track long stays by class and correct implausible durations
| | |
|---|---|
| **Finding** | Only 0.25% of encounters last over 24 hours, and 81.7% of those are inpatient (F3). Four encounters show durations longer than a year. |
| **Action** | Bed management reviews the 71 long-stay encounters, in particular the 58 inpatient ones. IT or records staff check why four encounters have an end time more than a year after the start. |
| **Benefit** | Keeps duration measures trustworthy, and shows where length of stay affects capacity. |
| **Limitation** | With only 71 cases, results are sensitive to individual records. The data has no discharge reason or outcome. |

### R5. Report medians and cost distribution, and review the highest-cost encounters
| | |
|---|---|
| **Finding** | The top 5% of encounters (about 1,394) carry 44.6% of claim cost (F4). |
| **Action** | Show the median next to the average in every cost report, and review the top 5% of encounters as a group to understand what drives them. |
| **Benefit** | Prevents decisions based on an average that no typical encounter resembles, and points review effort at a small number of cases. |
| **Limitation** | The data gives no clinical detail, so it cannot show whether high costs were appropriate. |

## 5. Data quality and limitations

- **One organisation only.** Findings describe this hospital and do not generalise.
- **Partial final year.** 2022 stops on 5 February 2022 and is excluded from the trend line.
- **Zero recorded coverage is ambiguous** (R1) and is labelled this way on the dashboard.
- **Costs are skewed**, currency is not stated, and 89 encounters have a claim cost of zero. They are kept and flagged.
- **Four invalid durations** (over one year) are excluded from duration measures only, and kept in every other measure.
- **Procedure base cost varies** for the same procedure and is not necessarily what was charged or paid.
- **No outcome data,** so nothing here is a statement about clinical quality.

All data-handling decisions (D1 to D8) are recorded in `01_data_quality_assessment.md`.

## 6. How the dashboard was validated

| Criterion | Result |
|---|---|
| **SC1:** numbers reconcile with an independent calculation | All 13 KPI values rebuilt from the raw CSV files by `src/validate_kpis.py` match the dashboard. Evidence in `docs/validation_independent_check.txt`. |
| **SC2:** filters behave correctly | Filtering by encounter class, payer and year returned the expected counts and costs. The class counts and year counts each add back to 27,891. Screenshots are in `dashboard/screenshots/`. |
| **SC3:** KPIs are reproducible | `docs/kpi_definitions.md` defines each KPI. Over 24h % was rebuilt from its written definition (71 ÷ 27,887 = 0.25%). |

## 7. Privacy

No patient names, addresses or other identifiers appear in the dashboard, the screenshots or the repository. Patient name and address columns are dropped when the data is loaded, birth date is reduced to birth year, and raw data and the Power BI file are excluded from GitHub.
