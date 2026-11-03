# 03 — Product brief · [agent name] · v1

> Session 3. One page. Start from `01_problem_statement.md` and `02_investment_memo.md` — do not start from a blank page.
> v1 in class (16 October). v2 before Session 4 (30 October), after your users: fill the last two sections.

**Team:** … · **Starting point:** P_ / bring your own · **Version:** v1 — [date]

## 1. Problem, user, do-nothing  *(from 01)*
- **Problem in one sentence (with a number):** …
- **User (persona):** … — goal: … — pain: …
- **Do-nothing baseline:** …

## 2. The process — as-is and to-be
| # | Step | Who today | Minutes | Error rate | Cost of an error | Automate / augment / keep human (test it fails) | Trust level (L1–L4 or person) | Minutes after | Metric for this step |
|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |
| 4 | | | | | | | | | |
| 5 | | | | | | | | | |
| 6 | | | | | | | | | |

**Where the pain sits (the two steps):** …
**The way back to a person (designed first):** …
**Where the governance line sits:** …

*Trust levels — same scale as Session 1: L1 suggests · L2 drafts, a person approves · L3 acts on a scope, a person samples · L4 acts alone under a threshold.*

## 3. Features — RICE and MoSCoW
| Feature | Reach / month (from 02_sizing.xlsx) | Impact (0.25–3) | Confidence (50/80/100 %) | Effort (person-weeks) | RICE | MoSCoW |
|---|---|---|---|---|---|---|
| | | | | | | |

- **MUST (≤ 4):** …
- **SHOULD:** …
- **COULD:** …
- **WON'T this time (≥ 5) — this is the out-of-scope list:** …
- **The feature that tests our flip assumption, and why it is a MUST:** …
- **The cut that hurt the most:** …

## 4. Data  *(from the six-question audit — details in governance.md)*
Sources · volume and labels · coverage by segment · legal basis · leakage · freshness: …

## 5. Model — one rung per part
| Part | Rung (1 rules · 2 classical ML · 3 pretrained model · 4 hybrid) | Why the rung below fails |
|---|---|---|
| | | |

## 6. Where it lives (integration surface)
Surface · speed needed · format · fallback · who sees the log: …

## 7. Success criterion — one sentence
> By [date], on [eval-set], at least [threshold = our flip point from 02_sizing.xlsx] of [tickets] [metric] — and [guardrail].

## 8. Risks and rollback trigger
- Top risks (from your Working Backwards FAQ): …
- **Rollback trigger (one line):** …

---
*v2 only — after the users (before 30 October)*

## 9. What the users changed
| Change | Evidence (who said / did what — e.g. “3 of 3 never opened the tab”) |
|---|---|
| | |

## 10. What they could not decide
(The threshold, the model, the legal basis… — and who or what decides instead.)
