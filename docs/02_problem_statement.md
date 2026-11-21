# Problem Statement

**Project:** Hospital Operations, Cost & Patient Flow Intelligence
**Programme:** AnalystLab Africa Experience Lab, Week 3
**Author:** NZAU
**Related document:** [01_data_quality_assessment.md](01_data_quality_assessment.md)

---

## 1. The challenge

The healthcare organisation wants a clearer picture of how its hospital operates: how many patient encounters it handles, what kinds of encounters those are, what they cost, who pays, and which procedures are performed most. Today this information sits in separate raw tables (encounters, patients, procedures, payers) and cannot be read at a glance.

## 2. The question this work answers

> **How have encounter volumes, encounter types, costs and payer coverage changed and differed across the recorded period, and which procedures account for the most activity and cost, so that managers can see where operational and financial attention is needed?**

This is broken into eight measurable questions (all from the Track A brief):

| # | Question | Area |
|---|---|---|
| Q1 | How have encounter volumes changed over time? | Operations |
| Q2 | Which encounter classes account for the largest share of encounters? | Operations |
| Q3 | What proportion of encounters lasted more than 24 hours, where timestamps are valid? | Operations |
| Q4 | How do total claim costs vary across encounter classes? | Finance |
| Q5 | How much payer coverage is recorded, and how many encounters have zero recorded coverage? | Finance |
| Q6 | Which procedures occur most frequently? | Operations |
| Q7 | Which procedures have the highest average base cost, given frequency and data limits? | Finance |
| Q8 | How do average total claim costs vary by payer? | Finance |

## 3. Why it matters

- **Capacity and staffing.** Knowing how volumes move over time and which encounter classes dominate helps managers decide where to place staff, rooms and equipment.
- **Long stays.** Encounters lasting more than 24 hours use beds and staff for longer. Knowing how common they are, and in which classes, supports bed and discharge planning.
- **Financial exposure.** Many encounters show zero recorded payer coverage. Understanding how many, and for which payers, shows where income may be at risk.
- **Cost drivers.** Claim costs are heavily skewed, so a small number of expensive encounters and procedures may drive most of the cost. Finding them is the first step to managing them.

## 4. Intended users and the decisions they make

| User | What they look at | Decision the findings can support |
|---|---|---|
| **Hospital operations manager** | Volume trends, encounter-class mix, long-stay share, procedure frequency | Where to allocate staff and capacity; which services are growing; which procedures drive workload |
| **Finance / revenue manager** | Total and average claim costs, payer coverage, zero-coverage counts, cost by payer and class | Which payers and encounter classes to review for billing and coverage gaps; where cost concentration is highest |

The dashboard therefore has two views, an **operations view** and a **finance view**, plus a shared overview page.

## 5. Scope

**In scope**
- Analysis of the six supplied files for the period 2011 to early 2022.
- A dashboard, KPI definitions, validation evidence and a written executive summary.
- Statistical investigation and, if time allows, a predictive model, built on the same cleaned data.

**Out of scope**
- Clinical judgement, diagnosis or treatment recommendations.
- Any analysis that identifies individual patients.
- Comparison with other hospitals or with external benchmarks.
- Forecasting future demand as an operational commitment.

## 6. Limitations of the available evidence

These come from the data inspection in the Data Quality Assessment.

1. **One organisation only.** Findings describe this hospital and cannot be generalised.
2. **Zero coverage is ambiguous.** The data cannot tell whether a zero means unpaid, denied, patient-paid or missing, even for insured patients (4,779 insured encounters have zero coverage).
3. **Partial years.** 2022 holds data only to 5 February, so it cannot be compared with full years.
4. **Cost meaning.** Currency and the exact meaning of "total claim cost" beyond the data dictionary are not specified, and 89 encounters have a total claim cost of zero.
5. **Skewed costs.** A small number of very large claims dominate averages, so averages alone can mislead.
6. **Implausible durations.** 4 encounters appear to last more than a year and are excluded from duration calculations only.
7. **No outcome data.** There are no clinical outcome or quality fields, so no statement can be made about quality of care.
8. **Repeat patients.** Patients appear many times, so encounters are not fully independent.
9. **Procedure costs vary.** The same procedure can have different base costs, so a single "cost of a procedure" is not well defined.

## 7. How success will be judged

Success criteria are defined in the next document (`03_success_criteria.md`).

## 8. Assumptions

- The supplied dataset pack is the complete source of truth for this project.
- Field meanings follow `data_dictionary.csv` where it matches the CSV files.
- "Encounter" means one row in `encounters.csv`.
- Duration means `STOP - START`, in hours.
- Findings are descriptive. They show what the data records and do not prove causes.
