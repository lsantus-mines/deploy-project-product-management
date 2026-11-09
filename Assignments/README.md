# Assignments — FlowAssist · condensed edition

PDFs revised on 6 November 2026. Antoine: **@antorabo75**; Colin: **@csib-wq**. Handles corrected in the project README, PDFs, HTML and source archives.

- Assignment 1: problem summary, diagnosis, hypotheses, baseline and six governance answers.
- Assignment 2: one-page memo, model, full Low/Base/High register, seven costs, sensitivity, build/buy, pricing and risks.
- Assignment 3: 7-page PDF; brief v2, Lean Canvas and brief v1 one page each, condensed annexes and an index of the 20 cases. The complete cases remain in the required CSV, included in the source archive.

Instructions that require human actions remain explicitly unattested: interviews, user tests, human labels and personal Git contributions. The original financial model's limitations remain flagged. The PDFs do not claim full compliance where evidence is missing.

Documentation update of 9 November: these PDFs and archives remain the 6 November S1–S3 editions, with their historical 20-case index. The current CSV holds 50 development cases; [the S4 report](../evals/report_v0.md), [the architecture](../04_architecture.md) and [the audit](../docs/DELIVERY_AUDIT.md) describe the recent changes. The current Markdown memo includes the economic corrections made explicit in the S2 PDF.

The Sources archives keep the required files in their original format along with the DOCX instructions. Earlier assumptions and unverified source claims are kept there for traceability; the explicit corrections in the PDFs take precedence. Build: from the root of the project-product-management repository, `/opt/anaconda3/bin/python Assignments/Sources/build_assignments.py`.

## Assignment 4 · 9 November 2026

[Condensed PDF — Prototype & Architecture](Assignment_4_Prototype_and_Architecture.pdf) · **4 pages**: results against the criterion, misses → spec v2, real architecture with checkpoints ⊘ and switch ⏻, components, fallbacks, governance, data and reproduction.

[Original sources archive](Sources/Assignment_4_sources.zip): prototype, spec, architecture, governance, 50 cases, before/after fixtures and results, grids and instructions. The PDF summarizes the documented elements without turning automated results into human validation. The archive is the 9 November snapshot; the Markdown files in the repository are the current versions.

Independent build (does not modify the S1–S3 editions): `/opt/anaconda3/bin/python Assignments/Sources/build_assignment4.py`. Editable content: `Sources/assignment4_content.md`; HTML: `Sources/Assignment_4.html`; pagination and hash checks: `Sources/validation_s4.json`.
