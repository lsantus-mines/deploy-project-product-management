# 03 — S3 delivery matrix · updated 9 November 2026

**Decision:** v2 design ready for S4; no claim of user validation, benchmark success or production readiness. Three conversations and a prototype try-out took place on 9 November; their limits are listed below.

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
| Three 20-minute conversations with past-behavior evidence | `03_user_research.md` §0; `research/interviews_2026-11-09.csv` | Done 9 Nov with three friends of the team (2 from past jobs, 1 in role); mostly scenario questions, so weaker past-behaviour evidence |
| Clickable surface with link and prompt | Prototype instructions and local HTML/CSS/JS v0.4 | Complete local surface; Vercel demo public and HTTP/asset verified; actual one-hour build duration unmeasured |
| Two users try one task thinking aloud | `03_user_research.md` §0 | Partly: participants tried DEMO-01 and liked it; no completion, time or hesitation recorded |
| What users changed / could not decide | Brief §§9–10; D06–D08 | Done: three changes with quoted evidence; D07 left to Ops/Legal |
| Spec skeleton | spec.md v1 | Complete S4 contract |
| 20 cases with input/action/evidence/handover/segment/origin | eval_set_v0.csv; label_design_review.csv | Complete proposed labels; manual labelling requirement unfulfilled |
| Every member authors at least one commit using own account | Git history | No new authorship attested in this revision; cannot be supplied by the assistant |

## Scope and evaluation discipline
The S3 surface supports tracing, ambiguous candidates, a compliance route and access denial. No live LLM, bank connector, customer message or financial action exists. D01–D05 refine safety and clarity inside the three MUST features. The 20 development seeds are not an unbiased held-out benchmark. Active-work savings include review and fallback time and require independent paired timing on pre-labelled eligible cases. The 41.2% hurdle is not replaced by a draft acceptance rate.

## Public demo handover

The primary repository belongs to BenjaminAHS; the synchronized v0.4 deployment copy belongs to lsantus-mines. Primary-push synchronization is [verified by a successful run](https://github.com/BenjaminAHS/project-product-management/actions/runs/41667205280). The existing Vercel project is owned by Team Montagne; its production deployment is Ready. [Public demo](https://deploy-project-product-management.vercel.app) returned anonymous HTTP 200 and matches all five v0.4 runtime assets; rendered browser checks remain unperformed. See [deployment handover](prototype/DEPLOYMENT.md). Publication exposes the extended local application; it does not establish the S4 pipeline or the performance criterion. S4 update: primary `034267c` and publication snapshot `8a8a2cf` were verified synchronized on 9 November. HTTP delivery of the updated engine was verified on 9 November: all five assets returned anonymous HTTP 200 and match the S4 sources.

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
`python3 scripts/verify_s3.py` (Python + Node.js) now checks 50 unique complete development cases, 15 proposed eligible cases, policy IDs, document links, HTML IDs, the identical brief/annex criterion and 32 domain/interaction scenarios. The original S3 seed is F01–F20; its design-review CSV still covers those 20 cases. See [verification report](prototype/verification.md). Browser rendering, screenshots, keyboard navigation, live authorization and model metrics have not been verified.

## Extended application v0.4
The local demo now executes intake → account/history pre-reading → scoped matching → source-based drafting/checking → human final review → recorded reply or specialist handover → lifecycle/audit/timing. Ten fixtures and custom synthetic cases are supported. [Coverage and remaining production integrations](docs/PRODUCT_COVERAGE.md). Deterministic checks are implemented; the model evaluator, live systems, shared authentication and protected persistence are not. S3 research/label/economic requirements remain unchanged.
