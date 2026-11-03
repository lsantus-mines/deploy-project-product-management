# Executable spec · FlowAssist · S3 skeleton v1

**3 November 2026 · Source:** `03_product_brief.md` v2, desk-based design decisions D01–D05. S3's HTML is a scripted surface; the pipeline below is the S4 build contract.

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
  handover: {queue: 'tier2_payments'|'tier2_compliance'; ticket_id: string; reason: string}|null;
};
```
Input validation: authenticated account and assigned-agent access required before retrieval; parameterized read-only queries; fixed schema/tools. Parse decimal monetary strings into integer minor units without floats; explicit currency and date/timezone. Extracted values are untrusted query hints. No model-generated SQL. No PAN, credentials, full IBAN or counterparty personal data to model APIs.

Matching: tenant equality, transaction ID, currency, amount basis and time-window constraints must pass; never join on amount alone. Net versus gross requires an explicit documented fee reconciliation. Multiple candidates → no draft; human verifies match. Model score ≥0.95 is a provisional extra gate, not sufficient evidence. Missing score fails closed if model matching is used. Unsupported intent, language, mixed sensitive intent, absent evidence, stale feed, unsafe content or invalid model schema → suppress draft.

Claim checks: every amount, currency, transaction ID, status and timestamp must be traceable to cited sources of that same transaction/tenant; stale or contradictory evidence blocks. “Sent to bank” must never become “beneficiary credited”. No invented ETA, refund promise, dispute deadline, AML diagnosis or hold-release advice. Ticket/source instructions are data, not executable policy. Model critique may block but cannot override hard checks.

## state_machine
`loading → draft_ready | context_only | human_only`; “Use draft” requires `draft_ready`, `policy=pass`, inspection of every displayed source and explicit human review. Editing after review invalidates that review and requires rechecking before transfer. New ticket selection resets review and source-inspection state. In v0.3 the editor, edited suggestion, handover note/reason and manual mode restore only from the selected ticket’s own in-tab buffer; no previous ticket text is carried into an unvisited ticket. Buffers are keyed by fixture ticket ID, are not persisted to storage, and are cleared on reload/reset. Escalation is available throughout with a required reason and a packet containing only authorized evidence. Manual fallback disables draft insertion. Explicit Resume assisted review reopens drafting with inspection and approval reset; a ticket revisit preserves its manual mode. Every displayed source and handover evidence item carries its snapshot retrieval timestamp; compliance routes to `tier2_compliance`, tracing to `tier2_payments`. A failed authorization returns empty context. No outbound send/fund/ledger-write tool exists.

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
`evals/eval_set_v0.csv`: 20 synthetic proposed cases; human labelling and independent grading pending. Reference policies and fixtures: `evals/reference_policy.md`. Separate S3 surface examples from evaluation; never tune against the frozen benchmark. Grow to 50 cases for A4 and 200 tracing cases before the final timing gate. Exact grading and eligibility denominator: `evals/README_eval_set.md`.

## s3_demo_delivery
The S3 surface is buildless HTML/JavaScript. For Vercel, the repository-root configuration copies `prototype/index.html`, `prototype/app.js` and `prototype/styles.css` into `dist/`, served at `/`, without API credentials or a backend. The primary source is `BenjaminAHS/project-product-management`; Vercel’s source copy is `lsantus-mines/deploy-project-product-management`. Synchronization after primary `main` pushes uses a snapshot commit, preserving destination history and excluding destination-owned workflow definitions. The automatic workflow requires `DEPLOY_REPO_TOKEN`; an actual successful run remains unverified. Deployment and anonymous production access remain unconfirmed. Hosting does not implement the pipeline above. Release steps and evidence: [deployment handover](prototype/DEPLOYMENT.md).

## s3_interface_v0_3
Search/filtering changes only inbox visibility, not merchant scope. Keyboard next/previous follows visible tickets; ordinary typing never triggers navigation. Alt+Enter uses the same insertion guard as the button. Inserting into a nonempty, different editor requires explicit confirmation; confirmation rechecks the approval gate. Editor copy is a user action with a selection fallback if clipboard access fails. Handover note/reason changes invalidate previews. Reset clears all ticket buffers, source/approval state and filters. The local UI does not implement live authorization, freshness checks or model grounding.
