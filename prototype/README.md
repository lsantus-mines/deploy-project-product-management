# FlowAssist · Payment operations workspace v0.4

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

Run `python scripts/verify_s3.py` (Python + Node.js) for artifact checks and **30 domain/interaction scenarios**. No npm installation is required. [Verification report](verification.md) states what remains unverified, including real browser rendering and live integrations.

Vercel builds from the repository root using [vercel.json](../vercel.json), copying the five runtime assets into `dist/`. Changes go to the primary repository and then [the deployment copy](DEPLOYMENT.md). [Changelog](CHANGELOG.md).
