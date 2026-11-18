# 05 — Metrics · FlowAssist

Session 5 deliverable, one section per move: place the number, decide when to stop, choose what to protect, derive the business metrics, make the judge trustworthy.

**Number rule.** Each number comes from `02_sizing.xlsx` (cited *Sheet!Cell*), `02_investment_memo.md`, `evals/report_v0.md` or a named repo file. Thresholds marked *decision* are team choices, not measurements. **Status, 18 Nov 2026:** §1–§4 complete; §5 needs people for the labels and the second grader.

## 1. Place the number — the five-level stack

| Level | Question | Our metric | Value today | Produced by · clock | Owner |
|---|---|---|---|---|---|
| 5 Business | Does it move the P&L? | Fully loaded cost per eligible tracing ticket | Baseline €10 (*Inputs!D9*); not measured with FlowAssist | A/B, then finance close · monthly | Head of Payment Operations + Finance |
| 4 Product | Do specialists adopt it and get the job done? | Active handling time per eligible tracing ticket closed with an approved reply | Baseline 18 min (S1 scenario); logged as `handling_ms` | A/B; `make metrics` meanwhile · weekly | Head of Payment Operations; PM |
| 3 Guardrails | Does it stay inside the lines, for everyone? | Critical exposures: draft on a human-only ticket, another merchant's data, missed attack | 0 drafts on 13 human-only cases; 0/50 foreign sources; 0/30 attacks missed | Attack set + eval set in CI; `check_failed` events · every PR, daily | PM + DPO |
| 2 AI system | Does the workflow complete the task? | Replies a specialist would send without editing | Grader 1: 15/15 drafts (15/50 cases). Second grader pending | Eval set + two graders + judge · each release | PM |
| 1 Component | Is each step right? | Expected route matched (router, match, policy check) per case | 50/50 development cases after fixes (first run 37/50) | `make eval` · every commit | Engineering |

FlowAssist is a rung-1 workflow (rules and templates, no model chooses a tool). Level 1 therefore measures deterministic components; retrieval hit@k does not apply because lookup is by reference.

## 2. Decide when to stop — the stop criterion

> **"We stop improving expected-route agreement on the development set at 50/50, because the level-2 metric no longer responds: all 15 drafts already pass grader 1, and the 35 no-draft cases are deliberate abstentions (13 human-only, plus ambiguous, stale or blocked). The next point would cost newly labelled held-out cases and a second grader, not engine work."**

- **Shape:** a step. Below 50/50 a wrong route can mean a wrong match; above it, more agreement on the same 50 exposed cases buys nothing. Those cases were consumed by fixes and cannot support a new claim (`report_v0` §4).
- **Cost of the next point:** labelling and grading time (evaluation line €22k/yr, *Decision!D10*), plus the parity and regression re-run on every engine change.
- **Revisable only by a number:** if the held-out v1 set shows a route accuracy below 95% *(decision)* on any language, engine work restarts on that segment.
- **Floor, not a stop:** zero drafts on human-only tickets, zero foreign data, zero attack misses. Any miss fails CI and blocks the release; it is never traded against speed.

## 3. Choose what to protect — hierarchy by segment

| Kind | Metric | Numerator / denominator | Threshold | Lag · owner |
|---|---|---|---|---|
| **Primary** | Active handling time per eligible tracing ticket | Σ active minutes on eligible tickets closed with an approved reply ÷ those tickets (median and p95) | saving ≥ 41.2% vs manual arm | same day · Head of Payment Operations |
| Guardrail | Critical exposures | human-only drafts + foreign-data replies + attack misses ÷ all tickets | **0** | real time · Head of Payment Operations |
| Guardrail | QA score of approved replies | weekly human QA score, 5% sample + all disagreements | ≥ 92/100 in every language | weekly · QA lead |
| Guardrail | Match precision | approved replies about the right transaction ÷ approved replies checked | ≥ 98% | weekly · QA lead |
| Counter-metric | Seven-day reopen rate | approved replies reopened within 7 days ÷ approved replies | ≤ manual arm + 2 pts (S1 baseline < 5%) | 7 days · Head of Payment Operations |
| Counter-metric | Manual handovers | eligible tickets handed to a person ÷ eligible tickets | ≤ manual arm + 5 pts | same day · PM |
| Counter-metric | Edit rate | approved replies that differ from the pre-filled draft ÷ approved replies | watched, no band: near 0 with rising reopens = rubber-stamping | same day · PM |

- **Segments, pre-registered:** merchant language (EN · FR · DE · other), plan (SMB · Enterprise), rail (SEPA · SWIFT), severity (routine · hard). Always reported per segment, never the average alone (Simpson).
- **Harm threshold** *(decision, copied to `governance.md` S5)*: one critical exposure stops assisted drafting everywhere. If the FR or DE reopen rate exceeds 1.5 × EN for two weekly reads, or QA falls below 92 in one language, that language goes to `suggest_only`.
- **Why language first:** our only judge disagreements were English messages answered in French or German (F22, F23, F25, F26; open spec line S5-M01).
- **Gaming and repair:** the primary rewards speed, so a specialist could approve without reading. The QA sample over-weights unedited approvals, and approval stays one explicit human action the system never ticks (PR #3).

## 4. Derive the business metrics — three, with expected effects

The expected effect is the **flip point**: a 41.2% saving of active time on eligible tracing work clears the €125k hurdle (`02_investment_memo.md`). The base guess is 48% (*Inputs!D22*).

| Business metric | Baseline | Expected effect at read date | Hypothesis about… |
|---|---|---|---|
| Active time per eligible tracing ticket | 18 min | ≤ 10.6 min (−41.2%); base guess 9.4 min (−48%) | a cited draft with verified facts replaces manual ledger and clearing lookups |
| Cost per eligible tracing ticket | €10 (*Inputs!D9*) | ≤ €5.88; base guess €5.20 | saved time becomes handling capacity, not idle time |
| QA score of approved replies | ≥ 92/100 today *(scenario)* | **Non-effect:** stays ≥ 92 in every language | speed does not cost correctness or tone |

Eligible volume: 12,000 tickets/month (*Inputs!D6*) × 50% tracing (*Inputs!D14*) × 75% answerable from ledger and clearing (*Inputs!D18*) = **4,500 tickets/month**.

```
Router + match + policy check right                      L1: 50/50 dev
 └─ drafts sendable without editing                      L2: 15/15 drafts, grader 1
     └─ cited draft used and approved                    L4: edit rate, handovers
         └─ active time −41.2% (flip) … −48% (base)      L4 primary
             └─ cost per eligible ticket €10 → ≤ €5.88   L5
                 └─ net value clears the €125k hurdle only above the flip point
 guarded by: 0 critical exposures · QA ≥ 92 · match precision ≥ 98%
 watched by: 7-day reopens · handovers · edit rate, per language
```

## 5. Make the judge trustworthy — evaluation plan

- **Eval set v1** (`evals/eval_set_v1.csv`): 200 synthetic inputs tagged in `origin`, stratified by language, plan, rail and severity. [`assignment5_sample.csv`](evals/v1/assignment5_sample.csv) selects the **100 cases** to label and a nested **30-case golden set** with proportional quotas.
  - **Labels: 0/100.** Earlier label rounds are not reused after the project rebuild. Labels are written by people before any run; AI-proposed labels must be disclosed per row.
  - The 50 v0 cases stay a development regression only.
- **Rubric** (`evals/README.md`, v1.1, written before grading): four binary criteria (right payment, no invented fact, no promise or action, sendable as is) and one verdict (`sendable` · `needs_edit` · `escalate`).
- **Human–human agreement: pending.** Two graders score the same 30 golden cases blind. Target ≥ 80%; below that, fix the rubric and re-measure.
- **Human–judge agreement:** OpenAI `gpt-6-luna` with the rubric as prompt (`evals/judge_prompt.txt`, `make judge`).
  - Today **11/15 = 73%** against grader 1 on development drafts, after one rubric fix (v1.0 scored 8/15). Below the 80% bar, so the judge is **not yet trusted** for release decisions.
  - 41/41 known-bad variants escalated, 0 over-accepted. The 4 disagreements are a real defect grader 1 missed (S5-M01), not judge noise.
  - The drafter uses templates, not an LLM, so judge and drafter share no model family.
- **Cadence:** eval set, parity and attack set on every commit (CI). Judge on every engine or template change, with the judge model pinned. A human re-grades 5% of judged replies plus every human–judge disagreement, weekly.
- **Red rows:** `evals/adversarial_v0.csv`, 30 attacks (OWASP LLM01, LLM02, LLM06, LLM09, legal and specialist routes), 30/30 caught; CI fails on any miss.
