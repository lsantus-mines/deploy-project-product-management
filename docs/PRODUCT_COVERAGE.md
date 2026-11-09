# FlowAssist v0.4 + S4 fixes — coverage of the P2 journey

The reference statement is **P2 · Agent-assist copilot for a fintech (B2B payments)** in `course/project_proposals.docx`. v0.4 runs the business journey in a self-contained demo. It does not claim to replace real payment systems.

| Problem step | Usable function in the application | Explicit limit |
|---|---|---|
| Ticket intake | Case creation, assigned merchant, language, priority, search and filters | Demo data; no Zendesk connection |
| Account pre-read | Plan, region, KYC/PSD2 flags and past tickets of the assigned merchant only | Public fixtures; the selector is not server-side authentication |
| Payment identification | Extraction of references, amounts and currencies; lookup filtered by merchant | EUR/SEPA and USD/SWIFT, deterministic rules |
| Wrong match | Never chooses by amount alone; reference, currency and amount checks; case kept context-only when in doubt | No probabilistic score and no production isolation guarantee |
| Ambiguous reference | On hold, reopen, entry of a merchant-supplied reference, new analysis | The operator confirms where the reference came from |
| Reading the sources | Ledger and clearing records viewable, IDs and timestamps, consistency check | Scenario clock fixed at 2 November; sources do not become fresh by reloading the page |
| Reconstruction | Summary and timeline computed from the selected payment; transmission vs. credit distinguished | No promise of arrival or settlement |
| Fees and net amount | Reconciliation in integer minor units; gross, documented fees and net shown separately | No FX conversion or guessed fees |
| Regulatory constraints | Account flags and routing for compliance, disputes or financial actions | No custom legal rule, chargeback date or hold release invented |
| Sourced reply | EN/FR/DE text generated from facts, citing the sources of the same payment | Local templates; no generative model connected |
| Evaluation before display | Gate on identity, consistency, freshness, amounts/statuses and citations | Rule-based check, **not** the evaluator model required for the P2 target version |
| Editing and approval | Source review, editable draft, invalidation after edits, overwrite protection, final check | Free rewording that rules cannot certify goes to human review; detected monetary errors stay blocked |
| Human communication | Copy to clipboard and explicit recording of a human reply in the demo | No message is actually sent; the close button contacts no customer |
| Handover | Reason required, authorized context, payments/compliance/disputes destination; handover recorded locally | No external queue is actually fed |
| Tracking and resolution | Open/waiting/escalated/resolved statuses, reopen and decision journal | Browser-local state; no multi-user collaboration |
| Measurement and quality | Visible time per case, manual pause, stop at terminal states, session dashboard and exports | Timing aid, not a causal measure of AHT, quality or savings |
| Traceability | JSON receipts, journal export and timing CSV; data stored in the tab | Journal editable in the browser, not an immutable server audit |

## Three demo journeys

1. **Normal payment:** DEMO-01 → open both sources → check the draft → insert it → check the final text → record the human reply and close → export the receipt.
2. **Ambiguity:** DEMO-02 → put on hold → reopen → enter `INV-A`, confirming the merchant supplied it → check the two new sources → review and close.
3. **Sensitive case:** DEMO-03 or DEMO-09 → view account/policy → choose the reason → prepare the handover → check the destination → record the handover → check the journal and session dashboard.

Other included cases: failed USD payment, returned payment, fee reconciliation, stale source and ledger/clearing conflict. The form can create up to 30 demo cases by reusing fixture references.

## Remaining production scope

Read connectors, server-side authentication/authorization, shared persistence, protected audit, the generation model and the evaluator model must be integrated and validated on authorized systems. User research findings, the proposed labels and the 41.2% criterion do not become validated because of this extension. The target A/B protocol stays randomized by agent; this demo's timings do not replace it.

Customer-facing autonomy and actions on funds remain excluded. The three MUST and five WON'T of the S3 deliverable remain the initial scope decision; v0.4 extends the local experience without reintroducing financial actions, autonomous replies or excluded sensitive advice.

## S4 update · 9 November 2026

The v0.4 journey is unchanged. The engine fixes concern references/amounts and checking a supplied confidence for a match declared as model-based. The 32 tests pass and the 50 development cases produce the expected states (15 drafts). No real model computes that confidence. The [S4 report](../evals/report_v0.md) separates these checks from human quality and time savings; the [publication record](../prototype/DEPLOYMENT.md) separates Git synchronization from HTTP verification.
