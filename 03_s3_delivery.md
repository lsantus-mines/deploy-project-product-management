# 03 — S3 delivery matrix · 3 November 2026

**Decision:** v2 design ready for S4; no claim of user validation, benchmark success or production readiness. The team has chosen to omit participant research. This matrix exposes the resulting assignment gap alongside completed work.

| Assignment requirement | Artifact / evidence | Status |
|---|---|---|
| Same agent and economic flip point from S1/S2 | Brief §§1,7; design §§1,7; S2 workbook/memo | Complete; 41.2% retained |
| As-is minutes, errors, costs and source types; two pain steps | Design §2 | Complete; unmeasured values labelled guesses |
| To-be decisions, failed automation tests, trust, fallback and metric per step | Design §2; spec workflow/state machine | Complete design |
| Eight sorted RICE candidates, ≤4 MUST and ≥5 WON’T | Design §3 | Complete: eight, three MUST, five WON’T |
| One model rung per component; lower-rung alternative | Design §5 | Complete design; alternatives still require S4 evaluation |
| Six data-audit questions, purpose/retention/isolation/gaps/trust | Governance Session 3 | Complete design; live-data approvals absent |
| One-sentence criterion: metric, flip threshold, guardrail, dataset, date | Brief §7, same sentence in design §7 | Complete target; not a measured result |
| Brief v1 → v2 and one-page Lean Canvas | Archived v1; current brief; AI Lean Canvas | Complete desk-based revision |
| Three 20-minute conversations with past-behavior evidence | User needs / design record | Not fulfilled: no conversations conducted |
| Clickable surface with link and prompt | Prototype instructions and local HTML/CSS/JS v0.3 | Complete local surface; Vercel configured, public URL pending; actual one-hour build duration unmeasured |
| Two users try one task thinking aloud | T01/T02 acceptance scenarios; state checks | Not fulfilled: technical checks do not replace participants |
| What users changed / could not decide | Brief §§9–10; D01–D05 design register | Responsibilities complete; changes are designer-led, not user evidence |
| Spec skeleton | spec.md v1 | Complete S4 contract |
| 20 cases with input/action/evidence/handover/segment/origin | eval_set_v0.csv; label_design_review.csv | Complete proposed labels; manual labelling requirement unfulfilled |
| Every member authors at least one commit using own account | Git history | No new authorship attested in this revision; cannot be supplied by the assistant |

## Scope and evaluation discipline
The S3 surface supports tracing, ambiguous candidates, a compliance route and access denial. No live LLM, bank connector, customer message or financial action exists. D01–D05 refine safety and clarity inside the three MUST features. The 20 development seeds are not an unbiased held-out benchmark. Active-work savings include review and fallback time and require independent paired timing on pre-labelled eligible cases. The 41.2% hurdle is not replaced by a draft acceptance rate.

## Public demo handover

The shared repository belongs to BenjaminAHS; its owner is arranging public visibility. Vercel configuration is tracked, but no successful deployment, project owner, production URL or anonymous browser check is confirmed. See [deployment handover](prototype/DEPLOYMENT.md). Publication will expose the existing static S3 interface; it does not establish the S4 pipeline or the performance criterion. Update the README and prototype record together once the production URL is verified.

## Working ownership and schedule
The following is a proposed division of work, not a record of completed work or signed approvals.

| Owner | Work package | Target |
|---|---|---|
| Lenny | Brief/README and cross-document consistency | 3 November |
| Anthony | Spec and prototype behavior review | 4 November |
| Antoine | Independent label review, if undertaken | 4 November |
| Benjamin | Independent label review and policy reconciliation, if undertaken | 5 November |
| Colin | Coverage and governance review | 5 November |
| Whole team | Review package and author individual contributions with own accounts | 6 November |

The assignment DOCX states 8 November 2026; the earlier template states Friday 6 November. Use 6 November as the packaging target. Future S4–S8 documents remain outside this S3 revision.

## Reproducible checks
`python scripts/verify_s3.py` on macOS checks 20 unique complete cases, seven proposed eligible cases, policy IDs, document links, HTML IDs, the identical brief/annex criterion and 44 prototype state assertions. See [verification report](prototype/verification.md). Browser rendering, screenshots, keyboard navigation, live authorization and model metrics have not been verified.
