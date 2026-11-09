# Delivery audit — available session instructions, 9 November 2026

This index concerns the supplied Assignments 1–4. The repository has no complete assignment instructions for later sessions; future governance headings do not establish delivered experiments.

| Session | Concrete artifacts and checks |
|---|---|
| 1 | README team/agent, quantified problem and source types, cause tree, AI-level comparison, four selection criteria, fictional launch release clearly marked, three testable hypotheses and non-zero baseline; six governance answers in `governance.md`. Root source wording aligned with the scenario boundary. |
| 2 | Editable `02_sizing.xlsx`; root one-page memo aligned with the existing PDF’s corrected economics; source register, seven costs, scenarios/probabilities, named hurdle, sensitivity and build/buy comparison in the Assignment 2 PDF. The workbook’s historical scenario limitations are retained transparently rather than silently changing the threshold. |
| 3 | Brief v1/v2, one-page canvas, process times/error rates as assumptions, RICE/MoSCoW, per-component rungs, governance data audit, clickable local app and deployment configuration; desk-based design synthesis and two executable task scenarios; three conversations on 9 November (two from past jobs, one in role) and a three-person prototype test (self-reported), adding D06–D10. |
| 4 | Four logical steps in the engine; unmodified Paylio replay recorded; 50 CSV cases with pre-existing expected labels and executable adapters; versioned baseline/current outputs; architecture, spec v2 and human checkpoints; 32 automated scenarios and 50/50 expected development states. |

## Evidence categories

Automated checks, synthetic scenarios and AI desk analysis are identified as such. Real conversations, participant observations, independent human judgements and individual authorship cannot be inferred from those artifacts. The supplied instructions require those activities; this index does not certify them. The historical Git log and blank human-review grids retain the authentic evidence boundary. Path-filtered Git history records BenjaminAHS, Lenny and antotototototo18 on Session 1 files; BenjaminAHS and Lenny on Session 2 files; Lenny on the Session 3 files. These are existing author records, not newly invented contributions.

## Reproduce

```sh
python3 scripts/verify_s3.py
python3 scripts/verify_s4.py
/opt/anaconda3/bin/python scripts/run_paylio.py
```

Paylio needs pandas/scikit-learn; the existing Anaconda environment provides them. `docs/evidence/s4/paylio-run.txt` captures the successful original starter run. The starter score is an automated citation heuristic.

## Release

Primary target: `BenjaminAHS/project-product-management`, `main`. After a successful push run `python3 scripts/sync_deploy.py`, confirm workflow synchronization, and run `python3 scripts/verify_production.py` before claiming updated production delivery. Primary `034267c` was pushed successfully on 9 November. Publication `8a8a2cf` was verified synchronized with zero changes/removals. Updated production HTTP delivery was verified on 9 November with `scripts/verify_production.py` (five assets, HTTP 200, matching hashes); the Actions run itself was not inspected because GitHub CLI was not authenticated.
