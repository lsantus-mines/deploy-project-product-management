# 02 — Investment memo · 9 November 2026

**CONDITIONAL GO** for further validation if paired active handling-time saving reaches **41.2%** on pre-labelled eligible tracing cases, with QA ≥92%, grounding-check precision ≥98% and zero critical exposures. These gates are not demonstrated by deterministic state agreement.

## How much?
The existing `02_sizing.xlsx` models 144,000 annual tickets at €10 per ticket. Its full-scope Year-1 base net value is **€141,340**: €174,892 gross time-equivalent value, less €19,848 expected operational errors, €704 inference/retries and €78,000 fixed/semi-fixed costs, plus €65,000 SLA/retention value. Adoption averages 46.25% from quarterly assumptions of 15%, 35%, 60% and 75%. Integration is €60,000 upfront, amortised at €20,000/year; annualised net value is not Year-1 cash profit.

| Annual scenario | Pessimistic | Base | Optimistic |
|---|---:|---:|---:|
| Net value | −€59,828 | €141,340 | €434,862 |
| Probability | 20% | 60% | 20% |
| Do nothing | €32,130 | €57,600 | €96,600 |
| Next-best project | €100,000 | €125,000 | €145,000 |

## How sure?
Expected value is **€159,810**, €34,810 above the base alternative and €102,210 above base do-nothing. Probability-weighted comparisons differ: €124,000 alternative and €60,306 do-nothing. All operating inputs are course scenario figures, assumptions or planning analogies, not observed company measurements.

The dominant guess is 48% time saving on eligible tracing work. Under the workbook’s full-scope assumptions, net annual value at tracing saving x is €26,437.54631 + €239,379.13125 × x. Break-even against €125,000 is 41.174%, rounded conservatively to **41.2%**. The tracing-only MVP cannot establish the business value attributed to disputes, compliance and strategic retention.

## What if we are wrong?
The downside is −€59,828. Low/High category shares in the historical workbook sum to 94%/106%, requiring reconciliation before investment. Inference and error costs are charged to time-equivalents rather than all assisted calls; charging inference to 54,654 eligible assisted base conversations yields about €2,200 rather than €704. The retained €0.035 allowance and €0.92 vendor scenario are planning inputs, not current commercial quotes. No API or vendor purchase is recommended on those inputs alone. The €15/€90/€150 operational error severities do not price catastrophic financial-data disclosure; CCO/DPO owns that risk and any critical exposure stops drafting.

## Compared to what?
Do-nothing assumes 4% annual efficiency improvement: €57,600 in Base. The named hurdle is the **Merchant Self-Serve Dispute & Reconciliation Portal**, €125,000/year in Base. Staffing avoidance is not an additional benefit to add again. Keep the economic threshold fixed while collecting paired human timings, including failed and manual fallback cases.

## Build, buy or orchestrate?
**Orchestrate**, conditionally: workbook judgement scores are 4.35 versus Build 3.15 and Buy 2.15. The limited comparable-cost scenario breaks even at approximately 56,266 equivalent resolutions/year. Actual billable outcomes, connectors, provider terms and security must determine the choice before investment. The local app is a deterministic prototype, not evidence of vendor or production readiness.

Trace: editable workbook; detailed registers and recalculation in `Assignments/Assignment_2_Sizing_Investment_Memo.pdf`; archived prior memo in `research/investment_memo_v1.md`. S4 result: `evals/report_v0.md`.
