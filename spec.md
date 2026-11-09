# FlowAssist specification · v2 · S3–S4

**Updated 9 November 2026 · Source:** `03_product_brief.md` v2, desk-based design decisions D01–D05 and user-driven decisions D06–D10 (9 November conversations and prototype test). The production pipeline below is the target integration contract; application v0.4 implements a local deterministic demonstration described at the end.

## problem
A Tier-1 specialist investigates fragmented payment records before replying. Provide a tenant-verified tracing timeline and cited editable draft in Zendesk, retain human sending, and test ≥41.2% active time saving on eligible tracing cases. Dispute/compliance tickets get a handover, not advice.

## user_workflow
```text
read       : authenticated session + ticket -> verified tenant + intent       (L1 suggestions)
retrieve   : tenant + validated entities    -> safe candidates + timestamps   (L3 internal)
match      : safe candidates + confirmation -> unique selected transaction    (person confirmation)
draft      : selected transaction + sources -> cited internal draft            (L2)
check      : draft + sources + policy       -> pass or block with reason        (rules + L2 review)
review     : passing draft + sources        -> editable inbox reply             (person only)
send       : human inbox action            -> customer                        (person only, outside copilot)
log        : state transitions              -> minimized audit event           (L4 metadata)
escalate   : any state + reason             -> Tier-2 context packet            (person action; safe fallback)
```

## io_contracts
```typescript
type Ticket = {
  id: string; text: string; language: 'en'|'fr'|'de'|string;
  authenticated_merchant_id: string; // server session, NEVER ticket text
  plan: string; region: string; received_at: string; // ISO-8601 UTC
};
type Source = {
  source_id: string; merchant_id: string; transaction_id: string;
  amount_minor: number; currency: string;
  status: 'pending'|'sent_to_bank'|'credited'|'failed'|'returned';
  event_at: string; fetched_at: string; version: string;
};
type Result = {
  state: 'draft_ready'|'context_only'|'human_only';
  transaction_id: string|null;
  match_score: number|null; // experimental score, not probability or access permission
  draft: null|{text: string; citations: {source_id: string; claim: string}[]};
  policy: 'pass'|'block'; reasons: string[];
  context: Source[]; // authorized and masked only
  handover: {queue: 'tier2_payments'|'tier2_compliance'|'tier2_disputes'; ticket_id: string; reason: string}|null;
};
```
Input validation: authenticated account and assigned-agent access required before retrieval; parameterized read-only queries; fixed schema/tools. Parse decimal monetary strings into integer minor units without floats; explicit currency and date/timezone. Extracted values are untrusted query hints. No model-generated SQL. No PAN, credentials, full IBAN or counterparty personal data to model APIs.

Matching: tenant equality, transaction ID, currency, amount basis and time-window constraints must pass; never join on amount alone. Net versus gross requires an explicit documented fee reconciliation. Multiple candidates → no draft; human verifies match. Model score ≥0.95 is a provisional extra gate, not sufficient evidence. Missing score fails closed if model matching is used. Unsupported intent, language, mixed sensitive intent, absent evidence, stale feed, unsafe content or invalid model schema → suppress draft.

Claim checks: every amount, currency, transaction ID, status and timestamp must be traceable to cited sources of that same transaction/tenant; stale or contradictory evidence blocks. “Sent to bank” must never become “beneficiary credited”. No invented ETA, refund promise, dispute deadline, AML diagnosis or hold-release advice. Ticket/source instructions are data, not executable policy. Model critique may block but cannot override hard checks.

## state_machine
`loading → draft_ready | context_only | human_only`; “Use draft” requires `draft_ready`, `policy=pass`, inspection of every displayed source and explicit human review. Editing after review invalidates that review and requires rechecking before transfer. New ticket selection resets review and source-inspection state. In v0.4 the editor, edited suggestion, handover note/reason and manual mode restore only from the selected ticket’s own in-tab buffer; no previous ticket text is carried into an unvisited ticket. Buffers are keyed by ticket key and stored in per-tab sessionStorage with schema checks and redaction of known sensitive patterns; reload restores text/outcome but never approval or source inspection. Reset clears all saved work. Escalation is available throughout with a required reason and a packet containing only authorized evidence. Manual fallback disables draft insertion. Explicit Resume assisted review reopens drafting with inspection and approval reset; a ticket revisit preserves its manual mode. Every displayed source and handover evidence item carries its snapshot retrieval timestamp; compliance routes to `tier2_compliance`, tracing to `tier2_payments`. A failed authorization returns empty context. No outbound send/fund/ledger-write tool exists.

## edge_cases
| Condition | Required outcome |
|---|---|
| No match / missing amount or reference | Context only; ask for missing facts; never fabricate record |
| Two same-amount payments / uncertain identity | Context only; request unique reference; Tier-2 if unresolved |
| Different tenant / forged merchant in body | No unauthorized data displayed or sent to model; block and security event |
| Currency differs / FX unclear | Context only; no conversion or inferred match |
| Net/gross differs but source explains fee | Use verified reconciliation and cite gross/fee/net; otherwise block |
| Unsupported language | Human only; no automatic translation into an unsupported segment |
| Dispute / KYC / suspected fraud, including mixed intent | Human only; no advice or deadline; route appropriate specialist |
| PII / credentials in text | Mask before model/log; on failed redaction use human-only route |
| Prompt injection in ticket or retrieved note | Ignore instruction; block unsafe draft; no scope expansion |
| Stale/conflicting feed | Context only; timestamps + reason, no asserted current status |
| Source cannot be opened / model/API timeout | Context only; preserve verified evidence and manual path |

## fallbacks
Prototype design defaults: clearing snapshot age ≤5 min at request time; retrieval timeout 2s, total pipeline timeout 10s; no silent retries after timeout. These are guesses for Ops/Engineering to validate. Null timestamps, model unavailable, malformed JSON, score <0.95 or failed claim check → `policy=block`, `draft=null`. Escalation packet: ticket ID, verified merchant, safe candidate IDs, source timestamps, block reason, agent note. Audit acceptance by the destination queue in S4; local HTML only simulates it.

## done_criteria
Use the exact criterion in brief §7: 200 frozen synthetic tracing cases, pre-labelled eligibility, ≥41.2% paired total human active time saving including failed/fallback cases, QA ≥92%, grounding precision ≥98% and zero critical exposures. Two independent graders review every output; unresolved disagreement fails pending adjudication. No production GO from this seed set, an unvalidated label or mock UI timing. Record p95 retrieval/draft latency separately from active human time.

## out_of_scope
CRM tag automation; autonomous merchant replies; dispute deadlines; KYC/AML explanation or release advice; refunds/settlement execution. Also no live bank connectors in S3, no model fine-tuning, unsupported-language drafting or customer chatbot.

## eval_set
`evals/eval_set_v0.csv`: 50 synthetic development cases (15 proposed eligible), expanded from the original 20 S3 seeds; human labelling and independent grading pending. Reference policies and fixtures: `evals/reference_policy.md`. Separate S3 surface examples from evaluation; never tune against the frozen benchmark. The 50-case A4 development run is recorded in `evals/report_v0.md`. A separate frozen 200-case tracing benchmark is required before the final timing gate. Exact grading and eligibility denominator: `evals/README_eval_set.md`.

## s3_demo_delivery
The S3 surface is buildless HTML/JavaScript. For Vercel, the repository-root configuration copies `prototype/index.html`, `prototype/app.js`, `prototype/data.js`, `prototype/engine.js` and `prototype/styles.css` into `dist/`, served at `/`, without API credentials or a backend. The primary source is `BenjaminAHS/project-product-management`; Vercel’s source copy is `lsantus-mines/deploy-project-product-management`. Synchronization after primary `main` pushes uses a snapshot commit, preserving destination history and excluding destination-owned workflow definitions. The automatic workflow uses `DEPLOY_REPO_TOKEN`; a push-triggered run for primary `e33deb3` was verified successful. Historical production evidence: the static demo was Ready at https://deploy-project-product-management.vercel.app on 3 November; anonymous HTTP access and all five v0.4 assets were verified byte-identical on 3 November 2026. Rendered browser checks remain unperformed. Hosting does not implement the pipeline above. The S4 snapshot `034267c` was subsequently pushed and its publication copy `8a8a2cf` verified identical on 9 November; updated HTTP delivery was verified on 9 November (five assets, anonymous HTTP 200, matching local files). Release steps and evidence: [deployment handover](prototype/DEPLOYMENT.md).

## s3_interface_v0_3
Search/filtering changes only inbox visibility, not merchant scope. Keyboard next/previous follows visible tickets; ordinary typing never triggers navigation. Alt+Enter uses the same insertion guard as the button. Inserting into a nonempty, different editor requires explicit confirmation; confirmation rechecks the approval gate. Editor copy is a user action with a selection fallback if clipboard access fails. Handover note/reason changes invalidate previews. Reset clears all ticket buffers, source/approval state and filters. The local UI does not implement live authorization, freshness checks or model grounding.

## application_v0_4_runtime
`data.js` supplies public synthetic accounts, history, policy and transactions. `engine.js` exports pure extraction, scope/match/freshness/schema/policy checks, grounded EN/FR/DE templates, draft screening and handover packet creation. Analysis runs on the fixture request clock, not today’s live bank data. Numeric amounts use integer minor units. An amount alone never authorizes a match; user-confirmed references still pass scope/currency/amount checks. A generated suggestion passes deterministic evaluation before display; it is not an LLM/model score. Free text not certifiable by rules requires explicit manual factual review, while detected critical edits remain blocked.

Lifecycle: `open → waiting | escalated | resolved`; reopen returns to `open` with review/inspection reset. A resolved outcome requires inspected sources, a non-critical final reply and explicit final human review. The action records a demo receipt; it does not send. Handover requires an up-to-date preview and explicit recording; reason/note edits invalidate it. Account history is scoped separately from transaction evidence and is never used to invent payment facts.

The tab-local journal and receipt exports are not immutable or authenticated. Visible-tab timings stop on pause, hidden tab, other views, intake/export interruption and terminal/waiting states; they are a workflow timing aid, not validated AHT or causal savings. Session restoration never restores approval. `node --test scripts/test_app.cjs` exercises current domain/UI behavior. Live APIs, shared identity/storage, LLM generation/evaluation and agent-level A/B remain unimplemented target integrations.

## Session 4 · spec v2 — changes of 9 November 2026

This section replaces the outdated S3 counts: 50 cases, 15 of them proposed eligible; all 50 are now development cases after the fixes. The production contract in the sections above does not become a shipped feature merely because it was evaluated.

| ID | Miss → v2 requirement | Status and validation |
|---|---|---|
| S4-M01 | A hyphen inside a reference is never a negative sign. A reference's digits never become an amount before EUR/USD. Genuinely negative amounts stay blocked. | Fixed in `entities` and `analyze`; dedicated regression and F01/F13/F14/F20/F21–F26/F49. Cases consumed for development. |
| S4-M02 | Also extract FAC-, RE- and REF-, without giving the reference any access power; keep account filtering and amount/currency constraints. | Fixed; F02/F03 and dedicated regression. |
| S4-M03 | Once a connector/model exists, explicitly represent the score and untrusted notes; missing score or <0.95 → abstention, notes never executed. | **Fixed**: `matchMethod=model` requires a finite numeric score in [0.95, 1]; unknown provenance blocked. `sourceRecords` and `makeDraft` ignore untrusted notes. F19 encodes the score and note from its original scenario; its label is unchanged. No real model is called. Tests cover missing, invalid and boundary scores, and a high score with a foreign account. |

Evaluation command: `node scripts/eval_s4.cjs`. Before/after kept in `evals/results_baseline_v0.json` and `evals/results_v0.json`. Two graders still have to judge the replies; state agreement ≠ sendability, grounding precision or time saving. Any fix made after reading a case turns that case into development data: a new independent set is required before any performance claim.

### S4 technical close-out
32 test scenarios pass; 50/50 expected states match, 15 drafts and zero drafts on human-only. All 50 remain development cases. F19 no longer contains an unrepresented contract field; the score is an input, not a measurement computed by a model. The original Paylio starter was run: heuristic 8/20 (40%), not a human grade. The Paylio teaching causes remain spec proposals: complete the Release notes 4.12 section (9 cases), review below-threshold routing for Add an admin user (2 cases) and Payslips as PDF (1 case), then test on a new set without tuning the threshold against these tickets.

### Runtime matching metadata (current code)

Synthetic transaction records may carry `matchMethod?: 'reference' | 'model'` and `matchScore?: number`. Missing method follows deterministic reference matching. Unknown method blocks; `model` requires a finite numeric score in [0.95, 1]. This input does not authorize retrieval and is checked only after merchant/reference/money/freshness/status/fee constraints. `sourceRecords` and `makeDraft` use allowlisted financial fields and ignore source notes. Snapshot age uses ticket `receivedAt` and allows 0–300,000 ms. Intake limits are 30 workspace tickets and 3,000 message characters; the offline 50-case evaluation is independent of these UI limits.

## user_driven_v2 · D06–D10 · 9 November 2026

From three conversations and a prototype test ([record](03_user_research.md)). Specified for v2; **not implemented in the prototype yet**.

| ID | Requirement | Acceptance check |
|---|---|---|
| D06 | Every context-only or handover reply tells the merchant the next step and when they will hear back. | Ambiguous (DEMO-02) and compliance (DEMO-03) replies name the next step and a follow-up time; no payment fact is added. |
| D07 | A draft may state a typical processing time for the rail only if FLOW-POL-1 documents it, labelled "typical, not guaranteed". Never a date for this payment, never for a returned or failed payment. Pending Ops/Legal approval. | With no documented time, no timing appears; with one, the label is present and the evaluator still blocks promises. |
| D08 | Status wording uses plain language next to the cited status (e.g. "sent to the recipient's bank, not yet confirmed as received" for sent_to_bank). | Each status maps to one approved plain phrase in EN/FR/DE; sent_to_bank never reads as received. |
| D09 | Above the draft, show a "verified facts" summary (transaction, amount, exact status, event time, sources inspected) that the specialist confirms before insertion. | Insertion stays disabled until every listed fact is shown with its source; edits that change a listed fact re-open the checklist. |
| D10 | Each source panel says what that record confirms (ledger: amount and booking; clearing: rail status and event time) and suggests opening the ledger first. | DEMO-01 shows both explanations; the wording never states beneficiary receipt for sent_to_bank. |
