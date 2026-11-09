# Session 4 — delivery status at 9 November 2026

Reference: `S4_templates/README_S4.md` and Assignment 4 (due 15 November, 23:59).

| Requirement | Deliverable / status |
|---|---|
| Executable prototype, four decisions | `prototype/engine.js`: classify → analyze rules → sourceRecords/makeDraft → evaluateDraft; interface with review and manual mode |
| 50 cases labelled before the run | 50-row CSV, AI-proposed labels; F21–F50 written before execution, S3 seed already exposed; reviewer 1 (Antoine, 9 Nov) approved 50/50; a second label reviewer is optional (A3 requires labels by hand, not two reviewers) |
| Run and number against the criterion | `node scripts/eval_s4.cjs`, before/after results and `evals/report_v0.md`; business criterion not demonstrated |
| Two independent graders | Grader 1 done (Antoine, 9 Nov: 15/15 sendable); grader 2 pending. Grading page `evals/grader.html`, merge `scripts/merge_grades_v0.py` |
| Three causes / spec v2 | Report and S4-M01–M03; three families fixed; no state disagreement on the 50 development cases |
| Architecture matching the real code | `04_architecture.md`, nine sections, checkpoints ⊘ and switch ⏻ |
| Governance S4 | `governance.md`: human checkpoints, switch owner/scope and storage |
| Four commits, four own authors | To be done by members with their own accounts. An assistant cannot fabricate contributions or rewrite history to satisfy this rule |
| Run the Paylio starter once | Done without modifying the starter via `/opt/anaconda3/bin/python scripts/run_paylio.py`. Routing 0.88; hit@3 1.00; heuristic 8/20 = 40% (threshold 45%); human-only 0. Evidence: `docs/evidence/s4/paylio-run.txt`. |
| S3: three conversations and brief v2 | Done 9 Nov: three conversations, a three-person prototype test (self-reported), brief v2 §9 with D06–D10 and quoted evidence |

The 50 cases were consumed for development after analysis: replace the benchmark before an independent measurement. No false verdict of success, time saving or validation by people.

Local checks: `python3 scripts/verify_s3.py` (32 domain/interface scenarios); `python3 scripts/verify_s4.py` (alignment of the 50 cases, grids, hashes and before/after rerun). The DOM harness is not visual browser evidence. Primary commit `034267c` was pushed; publication copy `8a8a2cf` was verified identical on 9 November. Updated HTTP deployment verified on 9 November: `scripts/verify_production.py` returns anonymous HTTP 200 and identical hashes for all five files.

Technical close-out: F19 resolved, 50/50 expected states, 15 drafts, 0 drafts on human-only; 32 tests. Real interviews, judgements and personal contributions are never replaced by an AI simulation.
