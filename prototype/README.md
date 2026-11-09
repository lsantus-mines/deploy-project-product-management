# FlowAssist · v0.4 workflow with S4 engine corrections · 9 November 2026

[Public demo](https://deploy-project-product-management.vercel.app). Open `index.html` locally as an alternative, keeping `styles.css`, `data.js`, `engine.js` and `app.js` beside it. The browser runtime has no dependencies, external assets, API credentials or build framework.

## The full workflow

Create a synthetic support request, inspect its assigned account and previous tickets, match a payment against scoped ledger/clearing fixtures, review a source-backed response, and explicitly record a human reply or specialist handover. Track open, awaiting-reference, escalated and resolved cases; reopen a case when information arrives. [Full P2 coverage and limitations](../docs/PRODUCT_COVERAGE.md).

Ten starting cases cover tracing, ambiguous references, compliance, denied references, failed USD transfers, returned payments, gross/fee/net reconciliation, stale snapshots, disputes and conflicting records. New cases can use the same fixture references, with a maximum of 30 cases. A merchant-confirmed reference can resolve an ambiguity; an amount alone never authorizes a match.

The account pane shows KYC/PSD2 flags and relevant prior tickets. Sensitive intents, unknown languages, mismatches, stale/malformed/conflicting sources and unsupported monetary inputs suppress drafting. Supported tracing replies are generated in EN/FR/DE from verified fields; rules check the generated text before display. There is no live LLM or model-grounding score. Free wording changes require human factual review; detected critical monetary/citation/promise errors cannot be recorded as an approved reply.

## Working safely and efficiently

Inspect every source, approve the suggestion, insert into the editor, then explicitly review the final response. Edits invalidate approval. Replacing different editor text requires confirmation. Manual mode and its resumption preserve the same review boundaries. Preparing handover requires a reason and includes only authorized source IDs/times; notes/reason edits invalidate the preview.

Copying, recording a reply, marking a case resolved or recording a handover stay local. No action sends customer messages, changes funds or contacts a real queue. The session dashboard reports actual local actions and visible-tab time, with pause for interruptions; it does not claim causal time savings, QA performance or the 41.2% business threshold.

Drafts, notes, outcomes, custom cases and activity are saved in **sessionStorage for this tab** and survive reload. Source inspection and approval never survive a ticket selection/reload. Reset demo clears the saved workspace. Known credential/IBAN patterns are redacted before storage; only synthetic data should be entered. Browser storage is not a secure payment datastore or immutable audit log. Storage failures fall back to memory.

Keyboard: `/` search; `J`/`K` next/previous visible ticket outside form fields; `Alt+Enter` insert an already reviewed draft; `Escape` close help/intake. The small-screen reading order follows the same DOM order. Activity, session metrics and exportable receipts are available from the navigation rail or mobile view buttons.

## Code and checks

- `data.js`: public synthetic accounts, transactions, historical context and policy fixtures.
- `engine.js`: pure extraction, scope/match/freshness/policy checks, grounded templates, edited-draft screening and handover packets.
- `app.js`: workflow, scoped ticket buffers, session storage, review state, audit/timing and exports.
- `styles.css`: responsive visual system; no remote fonts or component libraries.

Run `python scripts/verify_s3.py` (Python + Node.js) for artifact checks and **32 domain/interaction scenarios**. No npm installation is required. [Verification report](verification.md) states what remains unverified, including real browser rendering and live integrations.

Vercel builds from the repository root using [vercel.json](../vercel.json), copying the five runtime assets into `dist/`. Changes go to the primary repository and then [the deployment copy](DEPLOYMENT.md). [Changelog](CHANGELOG.md).

## Session 4

Reference formats FAC/RE/REF are supported alongside the existing formats. A reference suffix cannot be interpreted as a monetary amount or a negative sign. See [architecture](../04_architecture.md), [evaluation report](../evals/report_v0.md) and [delivery status](../04_s4_delivery.md). The 50-case development run is reproducible with `node scripts/eval_s4.cjs`; Antoine completed grader 1 (15/15 drafts sendable); grader 2 remains pending.

## Current engine contract

`analyze(ticket, data, confirmedReference)` scopes candidates to `ticket.merchant`, requires a unique reference, checks supplied monetary values and validates source fields. Snapshot age is measured against `ticket.receivedAt`, with a maximum of 300,000 ms (five minutes), never the computer’s current clock. The visible examples therefore remain reproducible.

Transaction fixtures may declare `matchMethod: "reference" | "model"`. For `"model"`, `matchScore` must be a finite number in [0.95, 1]; absent, string, out-of-range or low scores block drafting. Unknown methods also block. Omitted method retains the deterministic reference path. The runtime computes no model score; F19 supplies a synthetic input to exercise this gate. Source notes are excluded from `sourceRecords` and `makeDraft`.

`evaluateDraft` screens generated and edited text. Canonical drafts can pass local rules; noncanonical wording requires manual factual review, while detected critical errors block approval. `handover` produces only a local packet with authorized source IDs and timestamps.

`app.js` limits the workspace to 30 cases and intake messages to 3,000 characters. Those UI limits are separate from the 50-case offline development suite. `vercel.json` publishes only the five runtime assets; evaluation fixtures and coursework documents are not website assets.

## The four steps and their owners

One member owns and explains each step (Assignment 4: four commits, four authors). Each owner fills in their own subsection in a commit signed with their own account, named after the step.

### Step 1 · router: `classify` (`engine.js`) · owner: Anthony · commit `step-1-router`
- What it decides:
- Rung, and why the rung below fails:
- One failure or edge case seen (report or demo):
- Metric that would show it works:

### Step 2 · routing rule: gates in `analyze` (`engine.js`) · owner: Benjamin · commit `step-2-rule`
- What it decides:
- Rung, and why the rung below fails:
- One failure or edge case seen (report or demo):
- Metric that would show it works:

### Step 3 · drafter: `sourceRecords` and `makeDraft` (`engine.js`) · owner: Colin · commit `step-3-draft`
- What it decides:
- Rung, and why the rung below fails:
- One failure or edge case seen (report or demo):
- Metric that would show it works:

### Step 4 · policy checker: `evaluateDraft` (`engine.js`) · owner: Lenny · commit `step-4-policy`
- What it decides: whether generated or edited text can pass the local checks. No verified transaction or no `draft_ready` state is a critical block. Empty text, detected sensitive data, unsupported promises/actions, amounts/currencies/references, missing or foreign ledger/clearing citations and detected status upgrades are also critical blocks. A canonical EN/FR/DE template can pass; otherwise text without a detected critical issue still requires manual factual review (`passed: false`, `critical: false`). Passing never sends a reply: source inspection and final human approval remain required.
- Rung, and why the rung below fails: the shipped checker uses deterministic rules; its workflow is L2 assistance with person-only final approval. A simple copy-only template cannot check edits made after insertion. The proposed model-based grounding evaluator is not implemented; the rules do not certify arbitrary wording, translation, dates or every paraphrased promise. A person must compare the final text with the sources.
- One failure or edge case seen (report or demo): the automated scenario in `scripts/test_app.cjs` changes “was sent to the bank” to “was credited” and checks that approval is critically blocked (FLOW-POL-1 P03). The same scenario rejects a changed amount, foreign citation, invented reference and unsupported guarantee. Adding “Kind regards.” triggers manual factual review without a critical block. These are reproducible technical checks, not observations from a user session.
- Metric that would show it works: on independently labelled safe/unsafe draft pairs, report unsafe-detection precision TP/(TP+FP), recall TP/(TP+FN), false-safe count FN and the manual-review rate with denominators. Positive means flagged unsafe. No flagged drafts means precision is undefined. The ≥98% precision target and zero critical exposures are unmeasured; 50/50 development-state agreement does not measure checker precision or the ≥41.2% time-saving criterion.

Prepared with AI assistance for Lenny on 9 November 2026, from the implementation and automated scenarios; no independent human evaluation is attested here.
