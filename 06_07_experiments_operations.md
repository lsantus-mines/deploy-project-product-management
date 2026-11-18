# 06–07 — Experiments and operations · FlowAssist

## 1. Experiment design

**Comparison.** Run concurrent manual and assisted arms on pre-labelled eligible tracing work. Hold policy and release fixed. Include all assigned tickets, including fallbacks. Log interruptions and active work consistently. Blind the QA reviewers to assignment where feasible.

**Unit.** Randomise specialist shifts within specialist and week. Use one mode per shift and prevent reuse of drafts across arms. Track prior assisted exposure for learning carryover. Estimate uncertainty at shift level and report by language, plan and rail where samples permit.

**Three hypotheses.** At readout the assisted arm saves ≥41.2% of active time without increasing handovers by >5 points, achieves QA ≥92/100 without deterioration or critical escapes, and incurs no more than +2 points of seven-day reopens versus control.

## 2. Size and decision

**Smallest worthwhile effect.** A 41.2% time saving meets the S2 alternative-project hurdle. Measure blinded baseline variance and clustering and fix minimum enrollment before assignment.

**Read date.** Proposed ten business days of enrollment plus seven calendar days after the last case for reopens. Lock the calendar with the protocol. Review safety daily.

**Decision.** Expand to a limited next cohort only if the lower confidence bound reaches 41.2%, S5 limits pass and Finance validates cost inputs. Iterate on inconclusive results without critical harm. Stop immediately on critical harm and hold expansion when economics or quality fails. Head of Payment Operations signs with DPO review and Finance confirmation.

**Fallback.** If randomisation is infeasible, start in synthetic shadow mode, then compare before/after against a similar queue and document confounders. No real-ticket pilot result is available.

## 3. Monitoring

FastAPI is configured for Vercel. Use Vercel runtime logs and the local metrics report. Route pilot alerts to the owners below and test delivery before the pilot.

| Layer | Trigger | Cadence | Owner and action |
|---|---|---|---|
| Infrastructure | Errors >1% for ten minutes or API p95 >4 s. | Real time | On-call engineer checks traces and switches to manual if degraded. |
| Model/rules | Human–judge agreement <80% or failed release regression. | Weekly / release | PM reviews cases and suspends judge reliance. |
| Product and guardrails | Any critical escape or rejected reply rate doubles week on week. | Immediate / daily | Head of Payment Operations pauses or rolls back. |
| Business | Time gain <41.2%, QA <92 or reopens > control +2 points. | Weekly / readout | Head of Payment Operations and Finance pause expansion. |

Watch reference-format drift first. Compare no-match and manual-route rates by language and rail and check for changes in case mix.

## 4. Incident and rollback

| Class | Response |
|---|---|
| Caught | Count refusals and review repeated reasons. |
| Wrong reply | Correct via specialist and add a regression case. |
| Harmful | Stop assistance immediately and involve the DPO. |
| Outage | Continue manually, inspect traces and restore after a green smoke check. |

**Trigger** critical escape, unsafe reply released or red smoke test. **Owner** Head of Payment Operations by day, on-call engineer outside hours. **Action** set ASSIST_MODE to off, redeploy and verify draft insertion is disabled. Revert to the last green commit if needed. **Time** target under 15 minutes. **User impact** mode banner and manual handling. **Test date** 18 Nov 2026, local FastAPI rehearsal on a synthetic case. The on → off → on sequence returned HTTP 200 → 409 → 200 on insertion. Analysis withheld the draft in off mode. Production deployment and recovery time remain to be rehearsed.

The OpenTelemetry design uses a request trace with child spans for analysis and draft checks. Current structured JSON traces record latency, status, version and mode in Vercel runtime logs or the local event file. Proposed retention is 30 days pending DPO approval. Exclude ticket text, amounts, references and drafts.

## 5. Accountable decisions

| Decision | Owner |
|---|---|
| Approve experiment on real tickets | Head of Payment Operations with DPO review |
| Review weekly metrics | Product Manager |
| Activate rollback | Head of Payment Operations or on-call engineer |
| Manage trace access and deletion | Engineering lead with DPO review |
| Sign launch or hold | Head of Payment Operations with Product and Finance review |
