# Session 4 status — 9 November 2026

The CSV now contains **50 synthetic proposed labels**, including 15 proposed eligible cases. F01–F20 remain the exposed S3 seed; F21–F50 were labelled before execution. All 50 became development data after inspecting failures and correcting extraction. **No held-out performance claim is valid.** Human label approval and two independent output graders remain pending. `label_design_review.csv` covers only the original 20 cases. The historical S3 guidance below describes the original seed.

Run `python3 scripts/verify_s4.py` for artifact checks and both runs; use `node scripts/eval_s4.cjs` for the deterministic development report. See [report](report_v0.md), [architecture](../04_architecture.md), `fixtures_v0.json`, `results_baseline_v0.json`, `results_v0.json`, `label_review.csv` and `grader_reviews.csv`. The runner scores expected states and local checks, never human sendability or time savings.

# Historical S3 seed · F01–F20

At S3 delivery, `eval_set_v0.csv` contained **20 synthetic cases** with proposed expected actions and source references. All inputs and initial labels were AI-generated. **Human labelling required by the assignment is pending**: do not describe these as human-labelled, golden or frozen. At that S3 stage no prototype outputs or performance measurements existed; current development outputs are in the S4 report. `reference_policy.md` defines the fictional policy and source semantics.

## Before a run
1. Two team members independently read all inputs and source snapshots, correct/approve the expected outputs, handover and `eligible_for_timing`, and record their Git-authored review in `label_review.csv`.
2. Reconcile discrepancies with an Ops/domain reviewer (or identify classmates in role). Record rationale before execution; never change labels to fit outputs. Sign off through each member's own account; the assistant cannot supply these attestations.
3. Freeze a Git commit/hash and version of FLOW-POL-1. Keep surface demo tickets separate. If developers inspect/use a case to tune rules/prompts, mark it development and replace it for held-out testing. This seed is a design artifact already exposed to its author, not an unbiased held-out test.
4. Expand to 50 cases for A4, then 200 tracing cases for the timing gate. Preserve adversarial cases, add independent scenario families, remove near duplicates, and have people label eligibility before seeing output. No customer records from an internship/job.

## Columns
The template's nine columns are preserved. `hand_over_to_a_person=yes` means specialist/manual handling beyond normal L2 approval. `no — L2 approval required` still means a human checks and sends. Two added columns: `case_type` (easy/hard/adversarial/out_of_scope), `eligible_for_timing` (proposed pre-run answerability for the S2 automatable-share denominator). IDs F01–F20 are stable. Segment strings specify language, plan, region, rail/currency and severity.

## Scoring outputs
Two graders, independently and blind to each other's assessment, record per-case pass/fail: correct tenant+transaction, exact money/status/time, valid citations, safe intent handling, no promises, usable wording. “Usable as is” allows only cosmetic formatting, no factual edits. Unresolved disagreement is fail/pending adjudication, not automatic majority success. A wrong match or foreign-data exposure is a critical fail even if the prose is fluent. Proposed QA rubric: factual accuracy 40, source coverage 25, safe policy handling 25, clarity/language 10; wrong transaction/tenant or prohibited action fails regardless of points. Aggregate ≥92/100 is a design target, not a measured inherited company rubric.

Grounding-check precision = TP / (TP + FP), where positive means the checker **flags an unsafe draft**, TP is human-confirmed unsafe and FP is human-safe. Also report unsafe detection recall = TP / (TP + FN) and false-safe count FN; precision alone can miss dangerous drafts. No flagged items → precision undefined, never 100%. The 20 ticket seeds alone do not establish ≥98% precision; S4/S5 must curate safe/unsafe draft pairs including deliberate mismatches, with independent labels.

## Timing and denominator
The S2 workbook computes `eligible volume × time saved × adoption`, so 41.2% applies to **pre-labelled eligible tracing cases**, not all tickets and not the proportion of accepted drafts. For each eligible case collect manual active time M_i and assisted active time A_i (reading, verification, edits, handover, manual recovery included). Saving = `1 - sum(A_i)/sum(M_i)`. Do not discard model failures or fallbacks from eligible cases after running. Ineligible cases still test safe handover; report all-tracing coverage and unconditional time saving separately to check the 75% eligibility assumption.

Paired test: comparable agents, randomized/counterbalanced order and different equivalent cases to reduce memory/learning effects; log assignment, start/end active-work intervals and interruptions. Do not use the generic 18-minute assumption as each case's measured manual baseline. Report raw timings, participant count, median/range and uncertainty; a 20-case seed or a mock UI task is not a causal productivity estimate. Keep the economic threshold fixed; reaching it on synthetic cases warrants further validation, not immediate production approval.

## Coverage and status
Seven proposed eligible cases (F01–F04, F13, F14, F20), thirteen negative/fallback cases; catastrophic identity/status cases deliberately oversampled. EN/FR/DE and unsupported PT; SMB/Enterprise; EUR/SEPA and USD/SWIFT; all EU-region synthetic accounts. Segment results must show denominators; no population weighting inferred. Live timeouts, row-level security and backend permissions require S4 integration tests in addition to these input fixtures.

No pass rate, timing result, independent grader judgement or human label approval is claimed in S3. `label_review.csv` originally reserved 20 case IDs and now reserves all 50; `grader_reviews.csv` separately records output judgements.

## v2 label design review — 3 November 2026
`label_design_review.csv` records the policy references, proposed eligibility/handover and rationale for every case. This is an AI-assisted desk review against FLOW-POL-1, not independent human labelling or a measured model evaluation. No labels were changed to fit model outputs. `label_review.csv` remains reserved for genuine human review; no names, approvals or commits are invented. Structural checks are reproducible with `python scripts/verify_s3.py` on macOS.
