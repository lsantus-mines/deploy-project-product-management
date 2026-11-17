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

```text
project-product-management/
├── README.md · spec.md · governance.md     start here: overview, full spec, governance log
├── 00_pitch.md … 04_architecture.md        graded deliverables, course template names
│   (02_sizing.xlsx, 03_*.md; 05/06_07/08 to come)
├── Makefile · pyproject.toml · requirements*.txt · vercel.json · .env.example · AGENTS.md
│
├── prototype/      browser app (HTML/CSS/JS): preview engine, interface, API client
├── api/            FastAPI entry point on Vercel (/api/analyze · check · handover · events)
├── flowassist/     server engine, guardrails, switch, telemetry, server fixtures
├── tests/          pytest: JS/Python parity, API, attacks, metrics report
├── scripts/
│   ├── eval/       eval_s4 · run_adversarial · judge · metrics_report · export_data
│   ├── verify/     verify_s3/s4 · smoke · interface tests (Node)
│   ├── labelling/  eval-set generation and label/grade merges
│   └── deploy/     Vercel copy synchronisation
├── evals/          eval sets, attack set, judge prompt, reports (v0/ v1/ judge/ tools/)
├── docs/           setup (CI, deploy), tracking plan, delivery audits, S3/S4 annexes
├── research/       interviews, prototype test, archived brief and memo v1
├── pitch/          final deck: PDF, PPTX with speaker notes, notes mapped to the code
├── assignments/    submitted assignment PDFs and their sources
└── reference/      course material: slides and docs, S3/S4 templates, Paylio starter
```

### Deliverables by session

| File | Session | Status |
|---|---|---|
| `00_pitch.md` | before S3 — only if you bring your own idea | Present: optional adaptation of supplied P2, not a separate custom proposal |
| `01_problem_statement.md` | S1–S2 — Assignment 1 | Documented: quantified scenario, causes, AI choice, hypotheses and baseline |
| `governance.md` | created for Assignment 1, one line added every session | Updated through S7 draft: data audit, checkpoints, global switch, release approval, trace keeper |
| `02_sizing.xlsx` | S2 — Assignment 2 | Editable three-scenario model; financial limitations explained in the memo |
| `02_investment_memo.md` | S2 — Assignment 2 | Updated: conditional GO, named alternative and 41.2% flip threshold |
| `03_product_brief.md` | S3 | Brief v2 present; supporting process/design record and archived v1 |
| `04_architecture.md` | S4 | Implemented workflow, components, checkpoints, fallbacks; §8b server authority, switch and release path (v0.6) |
| `05_metrics.md` | S5 | To write (Assignment 5, 22 Nov). Inputs ready: [tracking plan](docs/TRACKING_PLAN.md), attack set, [judge report](evals/judge/judge_report.md), `make metrics` |
| `06_07_experiments_operations.md` | S6–S7 | To write (Assignment 6+7, 23 Nov). Inputs ready: switch, rollback, incident classes, monitoring thresholds in [spec.md](spec.md) §7 |
| `08_launch_memo.md` | S8 | Future session deliverable; not yet present |
| `spec.md`, `product_brief.md` | final | **`spec.md` v3: whole project S1–S7** (product, architecture, contracts, guardrails, operation, metrics, delivery, decision log); consolidated `product_brief.md` for the final push |
| `/prototype`, `/api`, `/flowassist`, `/evals` | from S4 | Interface v0.5 + FastAPI authority v0.6; 145 Python + 41 Node tests; 50 development cases, 200 held-out inputs, 30 attacks, LLM judge |

Supporting S3 files: [AI Lean Canvas](03_ai_lean_canvas.md), [design details](docs/03_design_details.md), [needs/design record](03_user_research.md), [prototype link](03_prototype_link.md) and [delivery matrix](docs/03_s3_delivery.md). S4: [report](evals/report_v0.md), [delivery matrix](docs/04_s4_delivery.md) and [evaluation guide](evals/README.md). [Cross-session evidence audit](docs/DELIVERY_AUDIT.md).

## Rules

- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.

## Current version · 17 November 2026

- **Interface v0.5** puts the user-test findings in the product: plain-language payment status (D08), a verified-facts checklist above the draft (D09) and guidance on which source to open first (D10).
- **Server v0.6** is the authority for every recorded action (FastAPI on Vercel). It also brings the global switch `ASSIST_MODE`, an attack set (30/30 caught), an LLM judge and local metrics.
- **Development set:** 50/50 expected states, 15 drafts, 0 drafts on human-only cases, no foreign source. These 50 cases were examined while building, so they serve as regression, not as a held-out performance claim.
- **LLM judge (`gpt-6-luna`):** see [evals/judge/judge_report.md](evals/judge/judge_report.md). It found a real defect the human grader missed: the reply language follows the ticket's language field, not the language the merchant wrote in.
- **Business criterion:** a 41.2 % active-time saving on eligible cases, measured with the paired protocol of S6. Not demonstrated yet.

The full specification is in [spec.md](spec.md) v3.

**Final pitch (17 slides, English):** [PDF](pitch/FlowAssist_Final_Pitch.pdf) · [PPTX with speaker notes](pitch/FlowAssist_Final_Pitch.pptx) · [speaker notes mapping each slide to the code](pitch/SPEAKER_NOTES.md).

## Server, guardrails and CI (v0.6)

The browser shows an instant preview; **the FastAPI server (`api/index.py`) decides every recorded action**: inserting a draft, recording a reply, recording a handover. The server uses only its own fixtures, so a client cannot inject evidence, and it refuses money promises, invented amounts, foreign references and status upgrades with HTTP 422. `tests/test_parity.py` keeps the browser engine and the server engine identical (123 cases, 468 draft checks).

| Command | What it does |
|---|---|
| `make install` | Python 3.12 venv + dependencies |
| `make dev` | API + prototype on http://127.0.0.1:8000 |
| `make ci` | lint, data sync, 144 Python + 41 Node tests, 50-case regression, 30-row attack set |
| `make adversarial` | OWASP-style attack set; one miss fails |
| `make judge` | LLM-as-a-judge on the graded drafts: OpenAI `gpt-6-luna`, key in `.env` (costs API credits) |
| `make metrics` | pre-launch metrics report from the local event file |
| `make smoke URL=…` | post-deploy check of page, health, config and one refusal |

- **Global switch:** env `ASSIST_MODE` (`on` / `suggest_only` / `off`; Vercel variable in production), any other value fails safe to `suggest_only`.
- **Metrics before launch, kept locally:** the page posts allowlisted events to our own server; `make dev` writes them to `metrics/events.jsonl` (git-ignored) and `make metrics` builds `metrics/report.md`. See the [tracking plan](docs/TRACKING_PLAN.md); no third-party analytics, no ticket text.
- **CI/CD:** `.github/workflows/ci.yml` on every PR and push; deployment to Vercel only after green CI on `main`, then a production smoke test. Setup: [docs/SETUP_CI.md](docs/SETUP_CI.md).
- **Evaluation:** [attack set](evals/adversarial_v0.csv), [grading guideline](evals/judge/rubric.md), [judge prompt](evals/judge_prompt.txt).

## Using the prototype

Open [prototype/index.html](prototype/index.html), or run from the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Then go to `http://127.0.0.1:8000/prototype/`: this static mode is a **local preview** (the banner says so; server guardrails are not active). Use `make dev` to run the real API with the page. No account or API key is needed. Drafts and actions are stored in the tab's sessionStorage; enter synthetic data only.

[Hosted demo](https://deploy-project-product-management.vercel.app). From v0.6, deployment runs only after green CI on `main` and is followed by an automatic production smoke test (`make smoke`). [Publication status and procedure](docs/DEPLOYMENT.md).

## Verify and reproduce

Python and Node.js are enough for the FlowAssist checks:

```sh
python3 scripts/verify/verify_s3.py
python3 scripts/verify/verify_s4.py
```

The first checks artifacts, links and 34 domain/interface scenarios. The second checks the 50 cases, review grids and hashes, then reproduces the initial and current runs. To rerun only the engine:

```sh
node scripts/eval/eval_s4.cjs
node scripts/eval/eval_s4.cjs --baseline
```

The Paylio starter needs pandas and scikit-learn. In the local environment where they are installed:

```sh
/opt/anaconda3/bin/python scripts/eval/run_paylio.py
```

On another machine, use a Python interpreter that has these dependencies. [Runtime instructions](prototype/README.md) · [Verification evidence and limits](docs/prototype_verification.md) · [Changelog](prototype/CHANGELOG.md).

## Assignment PDFs and sources

- [Assignment 1 — Team, agent and problem](assignments/Assignment_1_Team_Agent_Problem.pdf) · 4 pages.
- [Assignment 2 — Sizing and investment memo](assignments/Assignment_2_Sizing_Investment_Memo.pdf) · 6 pages.
- [Assignment 3 — MVP brief and design loop](assignments/Assignment_3_MVP_Brief_and_Design_Loop.pdf) · 7 pages.
- [Assignment 4 — Prototype and architecture](assignments/Assignment_4_Prototype_and_Architecture.pdf) · 4 pages · [original-format sources](assignments/Sources/Assignment_4_sources.zip).

[Package notes and reproduction](assignments/README.md). S1–S3 PDFs and archives retain their 6 November edition, including the historical 20-case S3 index; the current CSV has 50 development cases. The current Markdown documents describe the S4 code and results. Original instructions remain in `reference/course/`, `reference/templates/S3/` and `reference/templates/S4/`.

The documents distinguish automated checks, assumptions and human validation. They do not certify real conversations, independent judgements or individual contributions beyond the available evidence. Future deliverables in the template remain visible as future work rather than being omitted or described as completed.

## Source and publication

Develop in [BenjaminAHS/project-product-management](https://github.com/BenjaminAHS/project-product-management), branch `main`. Vercel uses the copy [lsantus-mines/deploy-project-product-management](https://github.com/lsantus-mines/deploy-project-product-management), which has a separate history. After every successful primary push, run `python3 scripts/deploy/sync_deploy.py` and confirm the result; preserve destination workflows and never force-push. [Repository instructions](AGENTS.md) · [Sync setup guide (French)](docs/ACTIVER_SYNC_GITHUB.md).

The S4 PDF delivery `60267d0` was pushed and its publication copy compared with no differences. Git synchronization is not an HTTP check of the site; dated evidence is kept in [the deployment guide](docs/DEPLOYMENT.md).
