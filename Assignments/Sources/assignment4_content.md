<div class="kicker">ASSIGNMENT 4 · PROTOTYPE & ARCHITECTURE</div>

# FlowAssist — build, evaluate, explain

<div class="meta">PayFlow B2B · P2 · 9 November 2026<br>Lenny Santus · Anthony Rascle · Antoine Rabeau · Benjamin Caujolle · Colin Sibieude<br>Due: 15 November 2026, 23:59 (Assignment 4 DOCX; workshop templates retain 6 November).</div>

**Job.** A copilot helps payment-support specialists trace a synthetic payment and prepare a cited EN/FR/DE reply. A person inspects the evidence and approves the final text; every recorded action remains local.

**Prototype:** [FlowAssist on Vercel](https://deploy-project-product-management.vercel.app) · [Source repository](https://github.com/BenjaminAHS/project-product-management). The current runtime uses rules and templates, with no live model, bank or Zendesk connection. The Git publication copy was verified; the latest successful HTTP asset check remains 3 November.

## 1. Evaluation v0 — the number against the criterion

**Criterion inherited from the brief:** ≥41.2% paired total active handling-time saving on pre-labelled eligible tracing cases in a frozen 200-case benchmark, QA ≥92%, unsafe-draft detection precision ≥98%, and zero critical exposures. A draft count is not this business criterion.

| Observation | Initial run | Corrected development run |
|---|---:|---:|
| Expected output states matched | 37/50 = 74% | 50/50 = 100% |
| Drafts produced with local policy check passing | 2/50 = 4% | 15/50 = 30% |
| Drafts on expected human-only cases | 0/13 | 0/13 |
| Cases with foreign-account sources in output | 0/50 | 0/50 |
| Outputs without a draft | 48/50 | 35/50 |

**Human sendability, QA and paired time saving:** not measured by these scripts. **Verdict: the business criterion is not demonstrated.** State agreement is not grounding precision. Intent routing alone is not scored independently; retrieval hit@3 is not applicable to exact-reference matching. No-draft counts include routing and missing/invalid evidence, not just policy blocks.

**Two-grader method.** Each person independently checks account/transaction identity, exact money/status/time, citations, safety and language, then answers “Would I send this without editing?” yes/no. Disagreements require adjudication; unresolved cases remain pending/fail. `label_review.csv` reserves label approvals and `grader_reviews.csv` reserves output judgements. Labels are AI proposals; no independent human judgement is inferred from automated checks.

## 2. Starter replay — separate from FlowAssist

The supplied Paylio starter was executed unchanged: routing accuracy **0.88**, retrieval hit@3 **1.00**, citation-based “sendable” heuristic **8/20 = 40%** against **45%**, human-only drafts **0**, policy blocks **0**. Its “sendable” column is an automated heuristic, not two graders’ opinion. Main misses: Release notes 4.12 (9 cases), Add an admin user (2), Payslips as PDF (1). Proposed spec changes are recorded without tuning the starter against these tickets.

<!-- PAGE -->

<div class="kicker">ARCHITECTURE · THE IMPLEMENTED WORKFLOW</div>

# Four steps, bounded decisions

## 3. Diagram — human checkpoints ⊘ and override ⏻

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 330" width="100%" height="280" role="img" aria-label="Four-step workflow with approval, abstention and manual override">
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#146e76"/></marker></defs>
<rect width="800" height="330" fill="#eff5f5"/>
<g fill="#ffffff" stroke="#91b7b8" stroke-width="1.2">
<rect x="15" y="25" width="140" height="44" rx="5"/><rect x="185" y="25" width="150" height="44" rx="5"/><rect x="365" y="25" width="160" height="44" rx="5"/><rect x="555" y="25" width="225" height="44" rx="5"/>
<rect x="555" y="110" width="225" height="48" rx="5"/><rect x="275" y="110" width="240" height="48" rx="5"/><rect x="15" y="110" width="220" height="48" rx="5"/>
<rect x="555" y="220" width="225" height="56" rx="5"/><rect x="275" y="220" width="240" height="56" rx="5"/><rect x="15" y="220" width="220" height="56" rx="5"/>
</g>
<g fill="none" stroke="#146e76" stroke-width="1.5" marker-end="url(#arrow)">
<path d="M155 47 H185"/><path d="M335 47 H365"/><path d="M525 47 H555"/><path d="M667 69 V110"/>
<path d="M555 134 H515"/><path d="M275 134 H235"/><path d="M125 158 V220"/>
<path d="M780 47 H792 V248 H780"/><path d="M667 158 V220"/>
<path d="M445 69 V90 H540 V248 H555"/>
<path d="M555 248 H515"/>
</g>
<g font-family="Arial,sans-serif" font-size="12" text-anchor="middle" fill="#243644">
<text x="85" y="44">Synthetic ticket</text><text x="85" y="59">+ assigned merchant</text>
<text x="260" y="51">1 · classify intent</text><text x="445" y="51">2 · routing rule</text>
<text x="667" y="44">3 · scoped lookup + match</text><text x="667" y="59">→ cited template</text>
<text x="667" y="138">4 · evaluateDraft policy check</text>
<text x="395" y="129">⊘ Inspect every source</text><text x="395" y="145">+ approve suggestion</text>
<text x="125" y="129">Editor → ⊘ final factual review</text><text x="125" y="145">Edits invalidate approval</text>
<text x="125" y="245">Record local reply / resolve</text><text x="125" y="261">No external send</text>
<text x="667" y="244">⊘ Human investigation</text><text x="667" y="261">No automatic draft</text>
<text x="395" y="244">⊘ Reason + current preview</text><text x="395" y="261">→ record local handover</text>
<text x="533" y="127" font-size="10">pass</text><text x="692" y="191" font-size="10">block</text>
<text x="640" y="90" font-size="10">unsupported / missing / invalid evidence → abstain</text>
<text x="400" y="310">⏻ Operator selects manual mode for one ticket/tab; resume resets inspection and approval.</text>
</g></svg>

| # | Component / implementation | Rung · pattern | Trust | Checkpoint ⊘ | Observed metric |
|---|---|---|---|---|---|
| 1 | `classify` in engine.js | 1 rules · routing | L1 suggestion | Abstain on sensitive intent | End-to-end states; no standalone routing score |
| 2 | `analyze`: language, scope, reference, evidence constraints | 1 rules · routing/chaining | L3 local read scope | Abstention when constraints fail | 50/50 expected development states |
| 3 | `sourceRecords`, `makeDraft` | 1 templates · chaining | L2 draft | Inspect every source, approve | 15/50 drafts; 0 foreign-source cases |
| 4 | `evaluateDraft` + UI final review | 1 rules · chaining | L2 checked draft | Approve again after edits | 0/13 human-only drafts; critical edits blocked |

These levels describe the project’s autonomy scale, not a security certification. Paylio’s educational ladder is 2/1/3/1; FlowAssist’s delivered components are explicitly **1/1/1/1**. No pretrained model or model evaluator is claimed.

## 4. Workflow or agent?

A **workflow**: the path and all branches are fixed in code; no model chooses its tools or next steps. This suits financial identity/status risks and supports explicit abstention. Moving up requires server authentication and authorization, read-only connectors, strict model-output schemas, timeouts and independent evaluation. Customer sending and financial actions stay human-controlled and outside this prototype.

<!-- PAGE -->

<div class="kicker">FAIL-SAFE BEHAVIOUR · GOVERNANCE · DATA</div>

# What blocks, who decides, where data lives

## 5. Fallbacks and runtime contracts

| Condition | Implemented response |
|---|---|
| No retrieval hit or no unique reference | No draft. Ask for a unique reference or prepare an authorized handover. An amount alone never confirms a transaction. |
| Low/missing confidence | For `matchMethod=model`, require a finite numeric `matchScore` in [0.95, 1]; otherwise abstain. Unknown methods block. The runtime does not compute this score. |
| Policy checker blocks | Critical monetary/citation/promise errors cannot be approved. Noncanonical wording needs manual factual review; rules do not certify arbitrary prose. |
| API unavailable | No API exists in this runtime. Live timeout behaviour is an integration requirement, not a completed test. Manual mode remains available; storage errors fall back to memory. |

Merchant scope, unique reference, supplied amount/currency, schema, consistent status and fee reconciliation must pass before drafting. Evidence age is **0–300,000 ms** against the ticket’s fixture request time. A high score cannot bypass these checks. Source notes are excluded from financial fields used to draft. UI intake allows **30 workspace cases** and **3,000 message characters**; the offline 50-case suite is separate.

## 6. Human checkpoints and override ⏻

**Approval:** source-by-source inspection and draft approval; final editor review; explicit local response/resolution; required reason, current preview and explicit handover recording. Editing invalidates the corresponding approval or preview. **Abstention:** sensitive/unsupported intent, missing or ambiguous identity, stale/invalid/conflicting evidence and failed policy checks. Evaluation is intended as an exhaustive independent review, not a sampling shortcut.

**Switch owner and scope:** the operator can select manual mode for one ticket in one browser tab. Insertion is disabled; resuming assistance clears source inspection and approval. There is no server-wide switch. Ops owns the future global stop mechanism before a real pilot.

**Switch test:** automated on **9 November 2026**, scenario “manual fallback and resume require a fresh inspection” in `scripts/test_app.cjs`; part of **32 passing domain/interaction tests**. This is code-level evidence, not a user study or a browser-rendering check.

## 7. Data, provenance and access

- **Demo:** `prototype/data.js`, ten public synthetic starting cases, fictional accounts, ledger/clearing fixtures and historical context. No training data or real customer exports.
- **Development evaluation:** `evals/eval_set_v0.csv`, **50** rows (F01–F50), **15** proposed timing-eligible cases. Every row contains input, expected action, evidence, handover, segment, origin and case notes; executable adapters live in `fixtures_v0.json`.
- **Separation:** F01–F20 were exposed S3 seeds. F21–F50 had proposed labels before execution. After failures were inspected and the engine corrected, **all 50 became development data**, excluded from future held-out claims. Labels were not changed to fit outputs. F19’s adapter now encodes the score/note already in its original scenario.
- **Storage/access:** CSVs, review grids and results are versioned with repository access and copied to the publication repository; they are not Vercel website assets. App drafts, notes and actions use per-tab sessionStorage, with known-secret pattern redaction and memory fallback. This is neither secure financial storage nor an immutable audit log. Use synthetic data only.

<!-- PAGE -->

<div class="kicker">SPEC V2 · REPRODUCTION · DELIVERABLES</div>

# Every observed miss becomes a requirement

## 8. Failure families → spec v2

| Miss / examples | Component | Required change and evidence |
|---|---|---|
| Reference hyphens/digits misread as negative amounts or monetary values. F01, F13, F14, F20, F21–F26, F49: 11 initial failures. | Extraction / routing constraint | **S4-M01:** separate reference and amount tokens; retain real negative-amount rejection. Corrected; regression tests added. |
| FAC/RE formats ignored. F02, F03: 2 initial failures. | Extraction / lookup | **S4-M02:** recognize FAC-, RE- and REF- while retaining scope, identity and money constraints. Corrected and tested. |
| Model-score/note contract not represented. F19: revealed after parsing correction. | Matching contract / policy | **S4-M03:** represent model provenance and score; fail closed below 0.95 or for invalid scores; ignore source-note instructions. F19 now abstains without changing its expected label. |

The first two families account for 13 initial disagreements. The third was uncovered later; it is not presented as a third equally frequent initial failure. All three are resolved on this development suite. Full text, before/after outputs and hashes are preserved in the repository.

## 9. Reproduce and inspect

```sh
python3 scripts/verify_s3.py     # artifacts + 32 domain/UI tests
python3 scripts/verify_s4.py     # 50 cases, grids, hashes, both runs
node scripts/eval_s4.cjs        # current development outputs
node scripts/eval_s4.cjs --baseline  # archived initial run
```

Python and Node.js suffice for FlowAssist. The unmodified Paylio replay additionally needs pandas/scikit-learn: `python scripts/run_paylio.py` with a suitable interpreter (locally `/opt/anaconda3/bin/python`). Its recorded output is `docs/evidence/s4/paylio-run.txt`.

**Version trace:** runtime source `56971d9` (documentation follow-ups do not change the engine); exact engine and fixture SHA-256 values are in `results_v0.json`. The original engine and adapter are preserved in `engine_baseline_v0.js` and `fixtures_baseline_v0.json`. The two runs intentionally use separately versioned fixtures; F19’s later representation is explicit.

## 10. Required original-format artifacts

| Assignment requirement | Repository artifact |
|---|---|
| Working prototype / four logical steps | `prototype/` and `scripts/test_app.cjs` |
| Report v0 and three misses | `evals/report_v0.md` |
| Architecture: diagram, component table, workflow, fallbacks, switch, data | `04_architecture.md` |
| Every miss marked in spec v2 | `spec.md`, S4-M01–M03 |
| 50 cases with labels, evidence and segments | `evals/eval_set_v0.csv`, `fixtures_v0.json` |
| Human checkpoints, switch ownership/test and data access | Session 4 section of `governance.md` |
| Independent label/output review records | `evals/label_review.csv`, `evals/grader_reviews.csv` |
| S3 starting documents | Brief v2, Lean Canvas, research/design record and prototype link |

This PDF is the concise readout; the companion source archive retains the required files in their original formats. Existing author records remain in Git. Four commits by four people, independent human grading and real S3 conversations cannot be certified by PDF generation or simulated with AI identities.

**Next build, three lines:** freeze a new held-out benchmark; collect independent judgements and paired timings; add authenticated read-only integrations and a global stop mechanism before a real pilot. The full three-category S2 economics are not validated by a tracing-only demonstration.
