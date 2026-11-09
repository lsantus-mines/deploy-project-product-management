# Eval report v0 — FlowAssist

**Date:** 9 November 2026 · **Set:** `evals/eval_set_v0.csv`, 50 synthetic cases · **Version:** files identified by SHA-256 in the JSON results; no `eval-v0` tag created and no invented author commits.

## 1. The number against the criterion
| Measure | Value |
|---|---|
| S3 brief criterion | ≥41.2% paired active-time saving on 200 eligible tracing cases, QA ≥92%, detection precision ≥98%, zero critical exposures |
| First run: drafts produced with the local check passing | 2/50 = 4% |
| First run: expected states matched | 37/50 = 74% |
| After the fix: drafts produced with the local check passing | 15/50 = 30%; now a development set |
| After the fix: expected states matched | 50/50 = 100%; does not mean 100% grounding precision |
| **Replies two people would send without editing** | **Not measured; not 0%** |
| Drafts on the 13 cases expected human-only | 0/13 |
| Sources from another account in the output | 0/50 cases; local check only |
| Outputs with no draft after the fix | 35/50; includes routing, ambiguity and blocks, not only the policy checker |
| Intent routing alone | Not measured independently |
| Retrieval hit@3 | Not applicable: deterministic lookup by reference, no top-k retriever |
| Paired active time, QA, detector precision/recall | Not measured |

**Verdict: criterion not demonstrated.** Neither the draft count nor state agreement replaces the economic criterion and the two graders. Paylio's generic 45% criterion does not replace the FlowAssist brief's criterion.

Reproduction: `node scripts/eval_s4.cjs` deterministically rewrites `results_v0.json`. `results_baseline_v0.json` preserves the first run; reproduce it with `node scripts/eval_s4.cjs --baseline` and the archived engine `engine_baseline_v0.js` (same hash). Output text and source IDs are kept per case. The CSV labels were not changed after the runs.

## 2. The three observed failure families
| # | Cause | Cases and frequency on the first run | Component | Spec v2 line |
|---|---|---|---|---|
| 1 | Reference hyphen read as a negative amount, or a reference's trailing digit absorbed as an amount | F01, F13, F14, F20, F21–F26, F49: 11 cases, two successive parser defects | extraction / rule | S4-M01: separate reference tokens from amounts; fixed, regressions added |
| 2 | FAC and RE formats ignored | F02, F03: 2 cases | extraction / retrieval | S4-M02: documented FAC/RE/REF formats accepted; fixed |
| 3 | Score 0.94 and source note not represented in the runtime | F19: hidden by the parsing defect on the first run, revealed after the fix; 1 case fixed at close-out | matching contract / check | S4-M03: model branch not shipped; score and note required before integration; fixed: explicit `matchMethod=model`, `matchScore=0.94` and an untrusted note in F19; abstention observed |

The first two families explain the 13 initial disagreements. The third was the only disagreement left after the parsing fix. It is now fixed: F19 keeps its original abstention expectation and explicitly supplies the score and note already present in its text. The engine rejects the 0.94 score. Source notes are not among the fields allowed for generation. All three families are resolved in the regression suite; this does not prove the production pipeline is complete.

## 3. Who graded, and how
No human grader has scored the outputs yet. The 50 labels and their technical adaptation are AI-proposed. `label_review.csv` holds the label approvals; `grader_reviews.csv` holds the two graders' independent judgements and the adjudication. The cells are deliberately empty. Each person scores account/transaction/amount/status/date accuracy, citations, safety and language, then answers yes/no to "would I send this text without editing?". An unresolved disagreement counts as pending/fail, never as an implicit success. Do not show one grader's opinion to the other before submission.

## 4. What is demo data and what is eval data
F01–F20 were an exposed S3 seed. F21–F50 were written and labelled before the first run; the labels were not changed to match the outputs. The seed fixtures are a manual AI adaptation of the descriptions, not a parser of real tickets. F19 now explicitly represents the score and note of its original scenario. The first run's engine and fixtures are archived separately in `engine_baseline_v0.js` and `fixtures_baseline_v0.json`. No expected label was changed. After the errors were examined and the engine modified, **F01–F50 are development cases** and are therefore excluded from any future held-out measurement. All remain useful for regression. The ten tickets in `prototype/data.js` remain the visible examples; they are not the denominator of this report.

## 5. Next step
Use the results as a development regression; the economic criterion requires a paired protocol and genuine human judgements. The Paylio starter was run unmodified: routing 0.88, hit@3 1.00 and heuristic score 8/20 = 40% (threshold 45%), zero drafts on human-only. Evidence: `docs/evidence/s4/paylio-run.txt`; reproduction: `/opt/anaconda3/bin/python scripts/run_paylio.py`. The word "sendable" in that script is a citation heuristic, not the opinion of two people.
