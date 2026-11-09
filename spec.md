# FlowAssist specification · v2 · S3–S4

**Updated 9 November 2026 · Source:** `03_product_brief.md` v2, desk-based design decisions D01–D05. The production pipeline below is the target integration contract; application v0.4 implements a local deterministic demonstration described at the end.

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
The S3 surface is buildless HTML/JavaScript. For Vercel, the repository-root configuration copies `prototype/index.html`, `prototype/app.js`, `prototype/data.js`, `prototype/engine.js` and `prototype/styles.css` into `dist/`, served at `/`, without API credentials or a backend. The primary source is `BenjaminAHS/project-product-management`; Vercel’s source copy is `lsantus-mines/deploy-project-product-management`. Synchronization after primary `main` pushes uses a snapshot commit, preserving destination history and excluding destination-owned workflow definitions. The automatic workflow uses `DEPLOY_REPO_TOKEN`; a push-triggered run for primary `e33deb3` was verified successful. Historical production evidence: the static demo was Ready at https://deploy-project-product-management.vercel.app on 3 November; anonymous HTTP access and all five v0.4 assets were verified byte-identical on 3 November 2026. Rendered browser checks remain unperformed. Hosting does not implement the pipeline above. The S4 snapshot `034267c` was subsequently pushed and its publication copy `8a8a2cf` verified identical on 9 November; updated HTTP delivery could not be confirmed due to DNS failure. Release steps and evidence: [deployment handover](prototype/DEPLOYMENT.md).

## s3_interface_v0_3
Search/filtering changes only inbox visibility, not merchant scope. Keyboard next/previous follows visible tickets; ordinary typing never triggers navigation. Alt+Enter uses the same insertion guard as the button. Inserting into a nonempty, different editor requires explicit confirmation; confirmation rechecks the approval gate. Editor copy is a user action with a selection fallback if clipboard access fails. Handover note/reason changes invalidate previews. Reset clears all ticket buffers, source/approval state and filters. The local UI does not implement live authorization, freshness checks or model grounding.

## application_v0_4_runtime
`data.js` supplies public synthetic accounts, history, policy and transactions. `engine.js` exports pure extraction, scope/match/freshness/schema/policy checks, grounded EN/FR/DE templates, draft screening and handover packet creation. Analysis runs on the fixture request clock, not today’s live bank data. Numeric amounts use integer minor units. An amount alone never authorizes a match; user-confirmed references still pass scope/currency/amount checks. A generated suggestion passes deterministic evaluation before display; it is not an LLM/model score. Free text not certifiable by rules requires explicit manual factual review, while detected critical edits remain blocked.

Lifecycle: `open → waiting | escalated | resolved`; reopen returns to `open` with review/inspection reset. A resolved outcome requires inspected sources, a non-critical final reply and explicit final human review. The action records a demo receipt; it does not send. Handover requires an up-to-date preview and explicit recording; reason/note edits invalidate it. Account history is scoped separately from transaction evidence and is never used to invent payment facts.

The tab-local journal and receipt exports are not immutable or authenticated. Visible-tab timings stop on pause, hidden tab, other views, intake/export interruption and terminal/waiting states; they are a workflow timing aid, not validated AHT or causal savings. Session restoration never restores approval. `node --test scripts/test_app.cjs` exercises current domain/UI behavior. Live APIs, shared identity/storage, LLM generation/evaluation and agent-level A/B remain unimplemented target integrations.

## Session 4 · spec v2 — changements du 9 novembre 2026

Cette section remplace les nombres S3 obsolètes : 50 cas, dont 15 proposés éligibles ; les 50 sont désormais de développement après correction. Le contrat de production des sections précédentes ne devient pas une fonctionnalité livrée du seul fait de l’évaluation.

| ID | Miss → exigence v2 | État et validation |
|---|---|---|
| S4-M01 | Un tiret à l’intérieur d’une référence n’est jamais un signe négatif. Les chiffres d’une référence ne deviennent jamais un montant devant EUR/USD. Les montants réellement négatifs restent bloqués. | Corrigé dans `entities` et `analyze` ; régression dédiée et F01/F13/F14/F20/F21–F26/F49. Cas consommés pour développement. |
| S4-M02 | Extraire aussi FAC-, RE- et REF-, sans donner de pouvoir d’accès à la référence ; conserver le filtrage par compte et les contraintes de montant/devise. | Corrigé ; F02/F03 et régression dédiée. |
| S4-M03 | Lorsqu’un connecteur/modèle existe, représenter explicitement score et notes non fiables ; score absent/<0,95 → abstention, notes jamais exécutées. | **Corrigé** : `matchMethod=model` exige un score numérique fini dans [0,95 ; 1] ; provenance inconnue bloquée. `sourceRecords` et `makeDraft` ignorent les notes non fiables. F19 encode le score et la note du scénario d’origine ; son label reste inchangé. Aucun modèle réel n’est appelé. Tests couvrant scores absents, invalides, limites et score élevé avec compte étranger. |

Commande d’évaluation : `node scripts/eval_s4.cjs`. Avant/après conservés dans `evals/results_baseline_v0.json` et `evals/results_v0.json`. Deux évaluateurs doivent encore apprécier les réponses ; concordance d’état ≠ sendability, précision de grounding ou gain de temps. Toute correction faite après lecture d’un cas transforme celui-ci en développement : nouveau jeu indépendant requis avant une revendication de performance.

### Résultat de clôture technique S4
32 scénarios de test passent ; 50/50 états attendus concordent, 15 brouillons et zéro brouillon sur human-only. Les 50 restent de développement. F19 ne contient plus de champ de contrat non représenté ; le score est une entrée, pas une mesure calculée par un modèle. Le starter Paylio original a été exécuté : heuristique 8/20 (40 %), pas une notation humaine. Les causes pédagogiques Paylio restent des propositions de spec : compléter la section Release notes 4.12 (9 cas), revoir le routage sous seuil pour Add an admin user (2 cas) et Payslips as PDF (1 cas), puis tester sur un nouveau jeu sans régler le seuil contre ces tickets.
