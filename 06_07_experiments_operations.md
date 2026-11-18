# 06–07 — Experiments and operations · FlowAssist

Prove the effect, then keep it alive. Five sections: prove, size and decide, watch, contain, own. Thresholds marked *decision* are team choices; volumes come from `02_sizing.xlsx`. No real-ticket experiment has run.

## 1. Prove the effect — hypothesis and design

**Hypotheses** (one per business metric, written before any assignment):

1. If specialists use FlowAssist drafts on eligible payment-tracing tickets, **mean active handling time** falls from the concurrent manual arm (planning baseline 18 min) to **≤ 10.6 min (−41.2%)** by the read date, **without** seven-day reopens exceeding the manual arm + 2 pts.
2. If specialists use FlowAssist drafts on the same tickets, the **audited QA score** stays **≥ 92/100 in every language** by the read date, with **zero critical exposures**.
3. If specialists use FlowAssist drafts on the same tickets, **manual handovers** on eligible work stay within the manual arm **+ 5 pts** by the read date, so time is not saved by pushing work elsewhere.

The outcome exists with and without the agent: active minutes and QA are measured in both arms. S4's 15/15 sendable drafts are draft quality, not an outcome.

**Design: A/B on specialist-days, randomised within specialist.**

- **Unit:** one specialist on one working day. Each day a specialist works fully assisted (`on`) or fully manual (`off`); within each week, each specialist gets the same number of each, in random order.
- **Why not tickets:** a specialist who sees drafts in the morning answers manual tickets differently in the afternoon (spillover).
- **Why not specialists:** 18 specialists (*Inputs!D7*) give 9 per arm, and the reopen guardrail would never be readable.
- **Remaining leak:** what a specialist learns on assisted days carries into manual days. This shrinks the measured gap, so the estimate is conservative. We record prior assisted exposure and report the first and second half separately.
- **Fairness of the comparison:** all eligible tickets assigned that day count, including fallbacks and handovers. QA reviewers are blind to the arm. Policy, templates and release are frozen for the whole test.
- **The chain:** shadow mode (S4, done on synthetic data) → this A/B → stepped rollout to 100% → a 5% manual holdout for 6 months to check the effect lasts.

## 2. Size it, decide before

**Sample size** (α = 5%, power = 80%; *assumption* = to replace with the pre-test measurement):

| Step | Value |
|---|---|
| Eligible volume | 12,000 × 50% tracing × 75% answerable = 4,500/month ≈ **214 tickets/working day** |
| Smallest effect worth seeing (MDE) | **13% time saving**: below it FlowAssist loses to do-nothing (€57.6k; net value = €26.4k + €239.4k × saving, `02_investment_memo.md`). Finance sets this, not the analyst. |
| Primary, 18 min baseline, SD 14.4 min *(assumption: CV 0.8)* | ~600 tickets per arm |
| Reopen guardrail, 5% → 7% *(S1 baseline)* | ~2,210 tickets per arm |
| Clustering by specialist-day (≈ 12 tickets, ICC 0.05 *assumption*) | × 1.54 → **~3,400 tickets per arm, ~6,800 in total** |
| Duration | 6,800 ÷ 214 ≈ 32 working days → **7 weeks** |

**The slowest guardrail sets the size:** the primary alone needs about 3 days, but reopens need 7 weeks. Halving the reopen tolerance to +1 pt would need about 4× the sample. Before randomising, we measure the real SD, reopen rate and ICC on two weeks of manual work and recompute; the numbers above are then frozen.

**Read date:** once, at **week 7 + 7 calendar days** (last reopens mature). No reading of the primary before that.

**Decision rule** (fixed with the protocol, before the first ticket):

- **Ship** (stepped rollout) if the saving is **≥ 41.2%** with its 95% interval excluding 0, QA ≥ 92 in every language, reopens ≤ manual + 2 pts and handovers ≤ manual + 5 pts.
- **Iterate** if the saving is **13–41.2%** with all guardrails green: one more cycle, same protocol, after fixing the largest failure segment (S5-M01 language first).
- **Kill** if the saving is **< 13%**, or any guardrail band breaks at a weekly safety read.
- **Stop early only on harm:** one critical exposure (draft on a human-only ticket, another merchant's data, a prohibited money commitment sent) stops assistance the same day. Never stop early on a good number.
- **Signs:** Head of Payment Operations, after DPO review and Finance confirmation of the €10 vs €6.88 cost per ticket (`02_investment_memo.md`).

**Four traps, pre-empted:** peeking (one read date); novelty (7 weeks, halves compared); segments chosen after the fact (language, plan, rail, severity pre-registered in `05_metrics.md`); Simpson (always per segment).

**Plan B if we cannot randomise:** two weeks of shadow mode on real tickets (drafts produced, never shown), then before/after against a comparable queue that keeps working manually, with the confounders written down (seasonality, staffing, policy changes).

**Build note:** per-specialist assignment is not coded. `ASSIST_MODE` is global today, and no assignment is built before the signature.

## 3. Watch the four layers

FastAPI runs as a Vercel Python function (`api/index.py`), which deploys only after green CI.

| Layer | Watch | Threshold that pages | Clock | Owner · tool |
|---|---|---|---|---|
| Infrastructure | API errors, p95 latency, `api_unavailable` | errors > 1% for 10 min · p95 > 4 s | real time | On-call engineer · Vercel runtime logs + production smoke test |
| Model / rules quality | weekly human sample (5% + disagreements) vs judge; sendable rate | human–judge agreement < 80% · sendable < 35% two weeks running | weekly / every release | PM · `make judge`, `make eval` |
| Product & guardrails | drafts on human-only tickets, `check_failed` and `guardrail_blocked` by code, handovers, FR/DE vs EN | any draft on a human-only ticket · FR or DE reopens > 1.5 × EN two weeks running | daily | Head of Payment Operations · `make metrics` report |
| Business | active time, QA, reopens, cost per eligible ticket | saving < 41.2% at read date · QA < 92 · reopens > manual + 2 pts | weekly / monthly | Head of Payment Operations + Finance · weekly shared sheet |

**Paging:** a Slack or Teams webhook from the Vercel log drain to the two switch holders *(target, not built; delivery is tested before the pilot)*. A threshold nobody is paged by is a screensaver.

**First drift to watch: data drift in reference formats.** A new rail, bank or invoice format means the router stops finding a unique reference and routes to a person. **Signal:** the manual-route and no-match rates by rail and language, compared week on week; a jump of more than 10 pts *(decision)* triggers a review of the rules on new labelled cases.

| Other drift | Signal | Response |
|---|---|---|
| Concept (policy changes) | a new payment or refund policy | re-label the golden set, date the rubric |
| Knowledge (stale sources) | evidence older than the freshness gate | drafting refuses; refresh connectors |
| Model (judge provider updates) | pinned `gpt-6-luna` version changes | re-run human–judge agreement before trusting it |

## 4. Contain the incident

**Incident classes** (`governance.md` S2's harm threshold separates "sent wrong" from "harmful"):

| Class | Example | How we see it | Action |
|---|---|---|---|
| Caught | policy check refuses a money promise added by the specialist | `check_failed` / `guardrail_blocked` events | count it; spec line if a code repeats weekly |
| Sent wrong | correct transaction, wrong status wording sent | seven-day reopen on an approved reply; QA sample | specialist correction, regression case, spec line |
| Harmful | draft on a human-only ticket, another merchant's data, refund promised | critical refusal bypassed, merchant complaint, DPO alert | **switch off now**, incident report within 24 h, DPO if data |
| Outage | API down or fixtures unreadable | errors > 1% for 10 min, `api_unavailable` | page fails closed to manual handling; restore after green smoke test |

**Rollback plan (6 fields):**

1. **Trigger:** any harmful incident; sendable < 35% on the weekly sample; QA < 92 in any language; a red production smoke test.
2. **Who decides:** Head of Payment Operations by day; the on-call engineer at night, who then wakes the Head of Payment Operations. Never only the person who wrote the code.
3. **Action:** first `ASSIST_MODE=suggest_only` (drafts visible, never insertable). Use `off` (humans only) for a harmful incident or outage. Revert to the last green commit if a release caused it.
4. **Time:** under 15 minutes, by one person, from the Vercel dashboard on a phone (environment variable + redeploy ≈ 1 min).
5. **What people see:** specialists see the mode banner ("drafts paused, answer as usual") and work manually. Merchants see no change. Traces keep logging.
6. **Last tested:** **18 Nov 2026, local**, by Antoine Rabeau. `scripts/verify/rehearse_switch.py`: on → suggest_only → off → on returned insert 200 → 409 → 409 → 200, and `off` withheld the draft ([evidence](docs/evidence/s7/switch-rehearsal-2026-11-18.txt)). **Not yet done:** the staging rehearsal with both switch holders, which is required before any pilot (Gate 2) and is then repeated quarterly.

**One trace per request (OpenTelemetry, in words).** One trace per ticket action, one span per architecture step: `classify` (intent route) → `match` (tenant-scoped lookup) → `draft` (template) → `policy_check` (critical / warning codes) → `human_decision` (inserted, edited, approved, handed over). Attributes: ticket id, segment (language, plan, rail), engine and template versions, assist mode, source ids, policy result, human decision, latency. No ticket text, amounts, references or draft text.

- **Today:** the server writes JSON traces with spans `analyze` and `evaluate_draft`, status, latency, engine version and mode (`flowassist/telemetry.py`). The finer spans and the OpenTelemetry exporter are the target.
- **Where it lives:** Vercel runtime logs, plus `metrics/events.jsonl` locally (git-ignored). **30 days** retention, pending DPO approval.

## 5. Own the system

| Decision | Owner | Written where |
|---|---|---|
| Run an experiment on real tickets | Head of Payment Operations signs; DPO reads | §1–2, `governance.md` S6 |
| Read the weekly numbers and act | PM, every Monday | §3 |
| Press the switch | Head of Payment Operations by day; on-call engineer at night | §4, `governance.md` S7 |
| Approve a release (rules, templates, judge model) | PM, with `make ci` and the eval re-run attached | `evals/README.md`, CI |
| Keep the trace; answer a merchant or regulator | Engineering keeps and deletes logs; Legal and DPO answer | `governance.md` S7 |

Until a pilot starts, the switch owner is **Antoine Rabeau** (`governance.md` S4). He hands it to PayFlow Payment Operations at Gate 2.
