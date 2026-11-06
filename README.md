# PayFlow B2B — Agent-Assist Copilot for B2B Payments

**Course:** Data & AI Product: From Diagnosis to Delivery (MSA-DAT07-04) · Albert School & Mines Paris-PSL · shared project with Agentic Workflows  
**Cohort:** M2-INTER-1  

## Team
| Name | Git handle | Also in the Agentic Workflows team? |
|---|---|---|
| Lenny Santus | @lsantus-mines | no |
| Anthony Rascle | @antotototototo18 | no |
| Antoine Rabeau | @antorabo75 | no |
| Benjamin Caujolle | @BenjaminAHS | no |
| Colin Sibieude | @csib-wq | no |

## Our agent
- **Starting point:** Proposal P2 — Agent-assist copilot for a fintech (B2B payments).
- **The company:** PayFlow B2B — European B2B payments fintech, 800 merchant enterprise & marketplace customers, 12,000 support tickets / month, support team of 18 Tier-1 payment operations specialists.
- **The job, in one sentence:** When a merchant opens a support ticket regarding a transaction, payout, or dispute, the agent pre-reads the merchant's account and transaction ledgers, flags regulatory constraints (PSD2 SCA, AML/KYC status), and drafts a cited response with transaction links in the Zendesk sidebar for the human agent to review, edit, and send.
- **Trust level per step (S3 scope):** L1 entity suggestions; L3 internal tenant-scoped retrieval with human transaction confirmation; L2 cited drafting and validation; person-only customer sending; L4 bounded audit metadata. The model score cannot authorize data access. Dispute/KYC requests route to specialists. See `governance.md` Session 3 for updates to the earlier L4 matching proposal.
- **One thing it must never do:** It must **never** send a reply directly to a merchant, **never** execute or promise a fund transfer, refund, or settlement release, and **never** match or disclose transaction details without cryptographically verified merchant account ID match (preventing cross-tenant data leakage).

## Repository structure
One numbered file per session. Every member authors commits in at least four of the numbered files.

| File | Session | Status | Description |
|---|---|---|---|
| `00_pitch.md` | before S3 | done | Half-page pitch & 7-point checklist (Proposal P2 adapted) |
| `01_problem_statement.md` | S1–S2 — Assignment 1 | done | Problem statement, 5 Whys, AI justification, press release, hypotheses |
| `governance.md` | created for S1, updated S2 | done | EU AI Act tier, GDPR basis, accountability, guardrails, cost-of-error owners |
| `02_sizing.xlsx` | S2 — Assignment 2 | done | Bottom-up financial model (3 scenarios, 7 cost lines, sensitivity, build vs buy) |
| `02_investment_memo.md` | S2 — Assignment 2 | done | One-page CFO investment memo (CONDITIONAL GO, €159.8k EV, 41.2% flip point) |
| `03_product_brief.md`, `03_design_details.md` | S3 | v2 design complete | Concise brief, process, sorted RICE, model tables; v1 archived |
| `03_ai_lean_canvas.md` | S3 | v2 aligned | All 14 blocks aligned with S1/S2 and the v2 brief |
| `03_user_research.md` | S3 | design synthesis complete | Three work situations, five decisions and two acceptance scenarios; no participant research |
| `03_prototype_link.md`, `/prototype` | S3 | full local workflow v0.4 | Intake, account context, scoped analysis, human review, lifecycle, audit and session timing |
| `spec.md` | S3 | skeleton v1 ready | Contracts, trust levels, edge cases and v2 acceptance behavior |
| `/evals/eval_set_v0.csv` | S3 | 20 cases with design review | Synthetic inputs and proposed labels; independent human approval absent |
| `04_architecture.md` | S4 | upcoming | Technical architecture, RAG pipelines, grounding evaluator, tool schemas |
| `05_metrics.md` | S5 | upcoming | Business & technical metrics, counter-metrics, eval-set definitions |
| `06_ab_protocol.md` | S6 | upcoming | Agent-level RCT experiment design, sample size calculation, MDE |
| `07_operations.md` | S7 | upcoming | Model monitoring, drift detection, incident playbooks, on-call runbooks |
| `08_launch_memo.md` | S8 | upcoming | Final launch memo, go/no-go criteria, executive readout |
| `product_brief.md` | final | upcoming | Consolidated deliverable for final oral defence |
| `/prototype`, `/evals` | S3 → S4 | S3 surface/seed ready; pipeline pending | Deterministic local workflow now; live connectors and model evaluation remain S4 work |

## Assignment PDFs

Concise PDF editions, with required details and source archives:

- [Assignment 1 — Team, agent and problem](Assignments/Assignment_1_Team_Agent_Problem.pdf) · 4 pages.
- [Assignment 2 — Sizing and investment memo](Assignments/Assignment_2_Sizing_Investment_Memo.pdf) · 6 pages; one-page memo followed by the model annex.
- [Assignment 3 — MVP brief and design loop](Assignments/Assignment_3_MVP_Brief_and_Design_Loop.pdf) · 7 pages; one-page briefs/canvas, concise annexes and a 20-case index; complete cases in the source CSV.

[Package notes and original-format archives](Assignments/README.md). Outstanding participant research, human label review and individual Git contributions are explicitly identified; PDF packaging does not establish their completion. Team handles: Antoine **@antorabo75**, Colin **@csib-wq**.

## Assignment 3 — delivery v2 · 3 November 2026

Start with [the brief v2](03_product_brief.md), [design details](03_design_details.md), [Lean Canvas](03_ai_lean_canvas.md), [specification](spec.md) and [prototype instructions](03_prototype_link.md). [The delivery matrix](03_s3_delivery.md) maps the assignment to every artifact and states the remaining limits. The original templates are preserved in `S3_templates/`; [brief v1](research/brief_v1.md) is archived for comparison.

- **Design:** six-step process, source types/error assumptions/trust/metrics; eight sorted RICE features, three MUST and five WON’T; component model choices; six-question data audit and updated governance.
- **Application v0.4:** ten starting cases and new-ticket intake; scoped merchant account/history; an executable deterministic matching/generation/checking engine; reference clarification; source review and final human approval; lifecycle/priority tracking; specialist handovers; sessionStorage restoration; local audit, receipt exports and measured visible-tab timings. [P2 coverage](docs/PRODUCT_COVERAGE.md), [runtime instructions](prototype/README.md) and [changelog](prototype/CHANGELOG.md). No live model or payment connector is claimed.
- **v2 decisions:** inspect every source before insertion, explain the missing reference directly, preserve snapshot times in handover, route compliance to its specialist and disable insertion during manual fallback. [D01–D05](03_user_research.md) trace these decisions to acceptance scenarios.
- **Application v0.4:** [open the public demo](https://deploy-project-product-management.vercel.app) or open [prototype/index.html](prototype/index.html) locally, or run `python -m http.server 8000 --bind 127.0.0.1` and visit `http://127.0.0.1:8000/prototype/`. No install, account or API key. Nothing is sent to a real customer, bank or queue.
- **Verification:** `python scripts/verify_s3.py` (Python + Node.js) checks document links, CSV structure/policy references, HTML IDs, shared success criterion and **30 domain and interaction scenarios**. [Verification limits](prototype/verification.md): no browser rendering/screenshot, live integrations or validated product performance.
- **Evaluation:** 20 self-contained synthetic cases and an [AI design review](evals/label_design_review.csv). Labels remain proposed; the [human review register](evals/label_review.csv) is reserved for actual independent approvals. Seven eligible cases test tracing; thirteen cover blocking/handover. No benchmark pass or time saving is claimed.
- **Research:** the team excludes participant interviews/tests. The research document therefore provides work situations, design rationale and reproducible acceptance scenarios. It does not claim interviews, user validation or compliance with that part of Assignment 3. Member-authored commits and human label approvals must also reflect actual actions.
- **Threshold:** ≥41.2% paired active-time saving on eligible tracing, with QA ≥92%, grounding precision ≥98% and zero critical exposures. This remains a target for a frozen 200-case benchmark; tracing alone does not establish the complete S2 business case.
- **Deadline:** the assignment DOCX states **8 November 2026**; the template states **Friday 6 November, start of S5**. Packaging target: 6 November, retaining 8 November in the stated evaluation criterion. No tests are backdated.

## Public hosting on Vercel

**Primary source:** [BenjaminAHS/project-product-management](https://github.com/BenjaminAHS/project-product-management), `main`. **Deployment copy:** [lsantus-mines/deploy-project-product-management](https://github.com/lsantus-mines/deploy-project-product-management), `main`. The copy is synchronized with the v0.4 application; its separate history is preserved. Product changes belong in the primary repository.

Every primary `main` push triggers [the sync workflow](.github/workflows/sync-deploy.yml), which copies the latest committed source into deployment `main` without force-pushing or replacing destination workflows. **Automatic synchronization verified:** [successful push-triggered run](https://github.com/BenjaminAHS/project-product-management/actions/runs/41667205280) for primary commit `e33deb3`. The workflow uses the configured `DEPLOY_REPO_TOKEN` secret. Setup, permissions and the local fallback are documented in [the deployment guide](prototype/DEPLOYMENT.md). **Guide en français à transmettre à Benjamin : [activer le secret Actions](docs/ACTIVER_SYNC_GITHUB.md).** Agents must also synchronize after their primary pushes, following [repository instructions](AGENTS.md).

**Live demo: [FlowAssist](https://deploy-project-product-management.vercel.app).** The v0.4 production deployment was verified Ready on 3 November 2026. All five assets returned anonymous HTTP 200 and match the local runtime files byte for byte. [Repeat the HTTP checks](scripts/verify_production.py). [vercel.json](vercel.json) copies only the prototype HTML, stylesheet, fixtures, domain engine and application JavaScript into `dist/`, serving the app at `/` without environment variables. The existing project is `deploy-project-product-management`, owned by Team Montagne; CLI login is verified as `lsantus-mines`. See [the prototype record](03_prototype_link.md) for verification limits. For immediate use, open [prototype/index.html](prototype/index.html) locally.

## Rules
- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.
