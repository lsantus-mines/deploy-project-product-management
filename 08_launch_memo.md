# 08 — Launch memo · FlowAssist

**To:** Head of Payment Operations, PayFlow B2B · **cc:** DPO, Finance · **Date:** 18 November 2026

## Decision

**NO-GO for live rollout. GO to prepare a controlled pilot**, subject to the Stage 0 and Stage 1 gates below.

FlowAssist helps Tier-1 specialists answer "where is my money?" tickets. It matches the payment inside the assigned merchant's records, shows the sources, and pre-fills a cited reply that a specialist must approve. It never sends, refunds or touches the ledger.

## Why: what we know and what we don't

| Claim | Evidence | Status |
|---|---|---|
| The workflow routes correctly | 50/50 expected states on development cases (first run 37/50) | ✓ development only: cases were used for fixes |
| It never drafts what a person must handle | 0 drafts on 13 human-only cases; 0/50 foreign sources; 30/30 attacks caught | ✓ synthetic; CI blocks any miss |
| Its replies are sendable | 15/15 drafts pass grader 1 | ✗ second grader and the 100 held-out labels pending |
| The judge can be trusted | 11/15 = 73% human–judge agreement | ✗ below the 80% bar; open language defect S5-M01 |
| It saves ≥ 41.2% of active time | none; base guess 48% (`02_sizing.xlsx`) | ✗ needs the A/B of `06_07` |
| We can stop it | switch rehearsed on → suggest_only → off → on, 18 Nov 2026 | ◐ local only; staging test with both switch holders pending |

The business case clears the €125k hurdle only above a 41.2% time saving, and only if the €10 cost per ticket holds (the headcount check gives €6.88, which falls below the hurdle). Nothing yet shows either.

## Launch plan and gates

| Stage | Gate to pass | Who signs |
|---|---|---|
| **0 · Now → 26 Nov** · synthetic | `make ci` green; S5-M01 fixed (reply in the merchant's language); 100 labels + 30-case human–human ≥ 80%; judge re-validated ≥ 80% | PM + Engineering |
| **1 · Staging** · real data, zero merchants | 2 weeks of shadow mode; measured SD, reopen rate and ICC replace the assumptions in the sample size; switch rehearsed in staging by both holders; paging webhook tested | Engineering signs readiness; DPO approves data handling and 30-day trace retention |
| **2 · Pilot** · A/B on specialist-days, 7 weeks + 7 days | `06_07` decision rule read once at the read date. One critical exposure stops assistance the same day | Head of Payment Operations, after DPO review |
| **3 · Expansion** · stepped to 100%, 5% holdout for 6 months | saving ≥ 41.2%, QA ≥ 92 in every language, reopens ≤ manual + 2 pts; Finance confirms the cost per ticket | Head of Payment Operations with Product and Finance |

## Risks we accept and how we contain them

- **Wrong match or another merchant's data:** deterministic tenant scope and policy check; any occurrence is harmful, triggering the switch to `off` and the DPO.
- **Rubber-stamping:** edit rate and seven-day reopens watched together; QA over-samples unedited approvals.
- **Language segment pays for the average:** results reported per language; FR or DE reopens > 1.5 × EN moves that language to `suggest_only`.
- **Rollback:** `ASSIST_MODE` to `suggest_only` then `off`, under 15 minutes, by the Head of Payment Operations or the on-call engineer (`06_07` §4).

## The ask

Approve Stage 1. Name the on-call engineer and the QA lead, and give DPO and Finance one review slot each before the pilot.

## Who did what

From the Git history (path-filtered authorship), to be confirmed by the team before `v1.0`:

| Member | Main contributions |
|---|---|
| Anthony Rascle | FastAPI server, global switch, attack set, LLM judge, CI/CD and deployment sync, interface v0.9, pitch deck |
| Lenny Santus | prototype engine and interface, spec v3, S1–S3 documents, S5–S8 first drafts and PDF builds |
| Antoine Rabeau | architecture, user research and prototype test, grader 1, switch owner, S5–S8 rework and switch rehearsal |
| Benjamin Caujolle | sizing and memo, CI workflow, pull-request reviews and merges |
| Colin Sibieude | *no commit recorded on `main`; contribution to be stated by the team* |

[Metrics](05_metrics.md) · [Experiments and operations](06_07_experiments_operations.md) · [Specification](spec.md) · [Brief](product_brief.md) · [Governance](governance.md)
