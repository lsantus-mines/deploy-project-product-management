# FlowAssist — Payment tracing copilot for specialists

**Course:** Data & AI Product: From Diagnosis to Delivery (MSA-DAT07-04) · Albert School / Mines Paris-PSL · shared project with Agentic Workflows

**Cohort:** M2-INTER-1

**Live demo: [open FlowAssist](https://deploy-project-product-management.vercel.app)**

## Team

| Name | Git handle | Also in the Agentic Workflows team? |
|---|---|---|
| Lenny Santus | @lsantus-mines | yes |
| Anthony Rascle | @antotototototo18 | yes |
| Antoine Rabeau | @antorabo75 | yes |
| Benjamin Caujolle | @BenjaminAHS | no |
| Colin Sibieude | @csib-wq | no |

## Our agent

- **Starting point:** P2 — Agent-assist copilot for a fintech (B2B payments). FlowAssist adapts the supplied proposal; `00_pitch.md` records the adaptation rather than a separate custom proposal.
- **The company:** PayFlow B2B, a European B2B payments fintech: 800 enterprise/marketplace merchant accounts, 12,000 support tickets per month and an assumed team of 18 Tier-1 specialists. These are educational scenario/planning figures, not observed company measurements.
- **The job, in one sentence:** When a merchant submits a payment-tracing request, FlowAssist matches a transaction within the assigned merchant’s synthetic records and prepares a cited EN/FR/DE status reply, producing an editable draft for the specialist’s approval and local recording.
- **Trust level per step:** L1 intent/entity suggestions → L3 scoped local read-only lookup with explicit source inspection and human match review → L2 draft and policy checks → person-only final approval and local response/handover recording. The local journal is application metadata, not authenticated L4 production auditing. The production design retains person-only customer sending. Model confidence never authorizes access; the runtime uses rules/templates and makes no live model, bank or Zendesk call.
- **One thing it must never do:** Send an autonomous customer reply, execute/refund/release funds, write a ledger, or expose a payment outside the assigned merchant and verified transaction. Missing/ambiguous identity, invalid evidence or sensitive intent suppresses drafting and returns the case to a person.

## Repository structure

One numbered file per session. Every member authors commits in at least four of the numbered files. This is the course requirement, not a certification of contributions.

| File | Session | Status |
|---|---|---|
| `00_pitch.md` | before S3 — only if you bring your own idea | Present: optional adaptation of supplied P2, not a separate custom proposal |
| `01_problem_statement.md` | S1–S2 — Assignment 1 | Documented: quantified scenario, causes, AI choice, hypotheses and baseline |
| `governance.md` | created for Assignment 1, one line added every session | Updated through S4: source boundaries, data, human checkpoints and manual override |
| `02_sizing.xlsx` | S2 — Assignment 2 | Editable three-scenario model; financial limitations explained in the memo |
| `02_investment_memo.md` | S2 — Assignment 2 | Updated: conditional GO, named alternative and 41.2% flip threshold |
| `03_product_brief.md` | S3 | Brief v2 present; supporting process/design record and archived v1 |
| `04_architecture.md` | S4 | Implemented workflow, diagram, components, checkpoints, fallbacks and data |
| `05_metrics.md` | S5 | Future session deliverable; not yet present |
| `06_ab_protocol.md` | S6 | Future session deliverable; not yet present |
| `07_operations.md` | S7 | Future session deliverable; not yet present |
| `08_launch_memo.md` | S8 | Future session deliverable; not yet present |
| `spec.md`, `product_brief.md` | final | `spec.md` v2 present; consolidated final `product_brief.md` not yet present |
| `/prototype`, `/evals` | from S4 | Executable local workflow, 32 tests, 50 development cases and before/after reports |

Supporting S3 files: [AI Lean Canvas](03_ai_lean_canvas.md), [design details](03_design_details.md), [needs/design record](03_user_research.md), [prototype link](03_prototype_link.md) and [delivery matrix](03_s3_delivery.md). S4: [report](evals/report_v0.md), [delivery matrix](04_s4_delivery.md) and [evaluation guide](evals/README_eval_set.md). [Cross-session evidence audit](docs/DELIVERY_AUDIT.md).

## Rules

- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.

## Current version · 9 November 2026

The local prototype implements the full journey: ticket creation, account context, account-scoped lookup, reference clarification, cited reply, source inspection, approval, manual handling and local handover. The engine uses rules and templates; it calls no model, banking system or Zendesk. No customer message or fund movement is executed.

- **32 domain/interface tests pass.**
- **50/50 expected states match** on the development cases; 15 drafts, zero drafts on human-only cases and no foreign source observed.
- The fixes cover references and amounts, plus abstention on a match declared as model-based with a missing, invalid or below-0.95 score. The score never replaces an identity or source check.
- The original Paylio starter was run: routing 0.88, hit@3 1.00, heuristic score 8/20 = 40% against a 45% threshold. That heuristic is not a human grade.

The 50 cases were examined during development: these results serve as regression, not as a performance claim on a held-out benchmark. The business criterion remains ≥41.2% paired active-time saving on eligible cases, QA ≥92%, detection precision ≥98% and zero critical exposures. The automated results do not demonstrate this criterion.

[Architecture](04_architecture.md) · [Eval report](evals/report_v0.md) · [S4 delivery](04_s4_delivery.md) · [Session audit](docs/DELIVERY_AUDIT.md) · [Product coverage](docs/PRODUCT_COVERAGE.md).

## Using the prototype

Open [prototype/index.html](prototype/index.html), or run from the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then go to `http://127.0.0.1:8000/prototype/`. No account, npm install or API key is needed. Drafts and actions are stored in the tab's sessionStorage; enter synthetic data only.

[Hosted demo](https://deploy-project-product-management.vercel.app). The Git publication copy was verified in sync with the S4 delivery on 9 November, and the HTTP check the same day confirms all five files (anonymous HTTP 200, identical hashes). [Publication status and procedure](prototype/DEPLOYMENT.md).

## Verify and reproduce

Python and Node.js are enough for the FlowAssist checks:

```sh
python3 scripts/verify_s3.py
python3 scripts/verify_s4.py
```

The first checks artifacts, links and 32 domain/interface scenarios. The second checks the 50 cases, review grids and hashes, then reproduces the initial and current runs. To rerun only the engine:

```sh
node scripts/eval_s4.cjs
node scripts/eval_s4.cjs --baseline
```

The Paylio starter needs pandas and scikit-learn. In the local environment where they are installed:

```sh
/opt/anaconda3/bin/python scripts/run_paylio.py
```

On another machine, use a Python interpreter that has these dependencies. [Runtime instructions](prototype/README.md) · [Verification evidence and limits](prototype/verification.md) · [Changelog](prototype/CHANGELOG.md).

## Assignment PDFs and sources

- [Assignment 1 — Team, agent and problem](Assignments/Assignment_1_Team_Agent_Problem.pdf) · 4 pages.
- [Assignment 2 — Sizing and investment memo](Assignments/Assignment_2_Sizing_Investment_Memo.pdf) · 6 pages.
- [Assignment 3 — MVP brief and design loop](Assignments/Assignment_3_MVP_Brief_and_Design_Loop.pdf) · 7 pages.
- [Assignment 4 — Prototype and architecture](Assignments/Assignment_4_Prototype_and_Architecture.pdf) · 4 pages · [original-format sources](Assignments/Sources/Assignment_4_sources.zip).

[Package notes and reproduction](Assignments/README.md). S1–S3 PDFs and archives retain their 6 November edition, including the historical 20-case S3 index; the current CSV has 50 development cases. The current Markdown documents describe the S4 code and results. Original instructions remain in `course/`, `S3_templates/` and `S4_templates/`.

The documents distinguish automated checks, assumptions and human validation. They do not certify real conversations, independent judgements or individual contributions beyond the available evidence. Future deliverables in the template remain visible as future work rather than being omitted or described as completed.

## Source and publication

Develop in [BenjaminAHS/project-product-management](https://github.com/BenjaminAHS/project-product-management), branch `main`. Vercel uses the copy [lsantus-mines/deploy-project-product-management](https://github.com/lsantus-mines/deploy-project-product-management), which has a separate history. After every successful primary push, run `python3 scripts/sync_deploy.py` and confirm the result; preserve destination workflows and never force-push. [Repository instructions](AGENTS.md) · [Sync setup guide (French)](docs/ACTIVER_SYNC_GITHUB.md).

The S4 PDF delivery `60267d0` was pushed and its publication copy compared with no differences. Git synchronization is not an HTTP check of the site; dated evidence is kept in [the deployment guide](prototype/DEPLOYMENT.md).
