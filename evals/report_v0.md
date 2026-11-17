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
| **Replies two people would send without editing** | **Grader 1 (Antoine, 9 Nov): 15/15 drafts = 15/50 cases. Grader 2 pending, so not yet a two-grader number** |
| Drafts on the 13 cases expected human-only | 0/13 |
| Sources from another account in the output | 0/50 cases; local check only |
| Outputs with no draft after the fix | 35/50; includes routing, ambiguity and blocks, not only the policy checker |
| Intent routing alone | Not measured independently |
| Retrieval hit@3 | Not applicable: deterministic lookup by reference, no top-k retriever |
| Paired active time, QA, detector precision/recall | Not measured |

**Verdict: criterion not demonstrated.** Neither the draft count nor state agreement replaces the economic criterion and the two graders. Paylio's generic 45% criterion does not replace the FlowAssist brief's criterion.

Reproduction: `node scripts/eval/eval_s4.cjs` deterministically rewrites `results_v0.json`. `results_baseline_v0.json` preserves the first run; reproduce it with `node scripts/eval/eval_s4.cjs --baseline` and the archived engine `engine_baseline_v0.js` (same hash). Output text and source IDs are kept per case. The CSV labels were not changed after the runs.

## 2. The three observed failure families
| # | Cause | Cases and frequency on the first run | Component | Spec v2 line |
|---|---|---|---|---|
| 1 | Reference hyphen read as a negative amount, or a reference's trailing digit absorbed as an amount | F01, F13, F14, F20, F21–F26, F49: 11 cases, two successive parser defects | extraction / rule | S4-M01: separate reference tokens from amounts; fixed, regressions added |
| 2 | FAC and RE formats ignored | F02, F03: 2 cases | extraction / retrieval | S4-M02: documented FAC/RE/REF formats accepted; fixed |
| 3 | Score 0.94 and source note not represented in the runtime | F19: hidden by the parsing defect on the first run, revealed after the fix; 1 case fixed at close-out | matching contract / check | S4-M03: model branch not shipped; score and note required before integration; fixed: explicit `matchMethod=model`, `matchScore=0.94` and an untrusted note in F19; abstention observed |

The first two families explain the 13 initial disagreements. The third was the only disagreement left after the parsing fix. It is now fixed: F19 keeps its original abstention expectation and explicitly supplies the score and note already present in its text. The engine rejects the 0.94 score. Source notes are not among the fields allowed for generation. All three families are resolved in the regression suite; this does not prove the production pipeline is complete.

## 3. Who graded, and how
**Grader 1:** Antoine Rabeau graded the 15 drafts on 9 November 2026 with `evals/tools/grader.html`: 15/15 "would send without editing". **Grader 2: pending.** `grader_reviews.csv` records grader 1; `scripts/labelling/merge_grades_v0.py` adds grader 2 and computes agreement and the final number. **Labels:** Antoine reviewed the 50 AI-proposed labels with `evals/tools/label_review.html` on 9 November and approved all 50; a second label reviewer is optional (A3 requires labels by hand, not two reviewers). The label review was done after grading the drafts, so the reviewer had already seen the outputs; the labels themselves were written before the runs and were not changed. Each person scores account/transaction/amount/status/date accuracy, citations, safety and language, then answers yes/no to "would I send this text without editing?". An unresolved disagreement counts as pending/fail, never as an implicit success. Do not show one grader's opinion to the other before submission.

## 4. What is demo data and what is eval data
F01–F20 were an exposed S3 seed. F21–F50 were written and labelled before the first run; the labels were not changed to match the outputs. The seed fixtures are a manual AI adaptation of the descriptions, not a parser of real tickets. F19 now explicitly represents the score and note of its original scenario. The first run's engine and fixtures are archived separately in `engine_baseline_v0.js` and `fixtures_baseline_v0.json`. No expected label was changed. After the errors were examined and the engine modified, **F01–F50 are development cases** and are therefore excluded from any future held-out measurement. All remain useful for regression. The ten tickets in `prototype/data.js` remain the visible examples; they are not the denominator of this report.

## 5. Next step
Use the results as a development regression; the economic criterion requires a paired protocol and genuine human judgements. The Paylio starter was run unmodified: routing 0.88, hit@3 1.00 and heuristic score 8/20 = 40% (threshold 45%), zero drafts on human-only. Evidence: `docs/evidence/s4/paylio-run.txt`; reproduction: `/opt/anaconda3/bin/python scripts/eval/run_paylio.py`. The word "sendable" in that script is a citation heuristic, not the opinion of two people.

## 6. LLM judge (17 November 2026)
Guideline [`evals/judge/rubric.md`](judge/rubric.md), judge prompt = the guideline, copied; model OpenAI `gpt-6-luna` (`scripts/eval/judge.py`). Inputs: the 15 drafts above plus known-bad variants made by injecting one defect (wrong amount, refund promise, status upgrade on a non-credited payment), whose correct verdict is "escalate" by construction.

| Run | Human–judge agreement (grader 1) | Known-bad escalated | Over-accepted |
|---|---|---|---|
| v1.0 guideline ([report](judge/judge_report_v1.0.md)) | 8/15 = 53 % | 44/45 | 1 (our variant was wrong: F04 is credited) |
| **v1.1 guideline** ([report](judge/judge_report.md)) | **11/15 = 73 %** | **41/41** | **0** |

**Reading the disagreements (the course's step 5).** v1.0 disagreements came from two guideline ambiguities (the judge wanted the merchant ID in the reply; it read "not confirmed" as an invented fact) and one badly built variant. We fixed the guideline once (v1.1) and re-measured.

All four remaining disagreements (F22, F23, F25, F26) are the same **real defect that grader 1 missed**: the merchant wrote in English, but the draft is in French or German, because the reply language follows the ticket's `language` field rather than the message. Spec line S5-M01: the reply language must match the language the merchant wrote in; on a mismatch, flag it for the specialist.

**Limits.** 15 cases is a small sample. Grader 1 also reviewed the labels, and grader 2 is still pending, so there is no human–human agreement yet. In production the judge grades everything, and humans re-grade a random 5 % plus every disagreement, weekly.
