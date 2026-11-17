# FlowAssist interface changelog

## v0.8 · one guided flow in three steps · 17 November 2026

> **Status: design hypothesis, not a user finding.** Unlike D08–D10, v0.7 and v0.8 were not tried by users yet. They are retested with 5 users before any pilot; gate: 4 of 5 finish a ticket without help. Automation-bias watch: a pre-filled reply can be approved without reading, so the edit rate and the 7-day reopen rate are tracked as counter-metrics.

- The workspace is rebuilt around three numbered steps in one column: **1 Check the payment** (amount, plain status, open the ledger then the clearing record) → **2 Review the reply** (one editor, pre-filled with the cited draft as soon as both records are opened, verified facts beside it) → **3 Approve & close** (one checkbox, one button). The current step is highlighted; the others are dimmed or ticked.
- Tickets that can't be drafted show one clear card instead (why, and the reference to ask for) with the specialist handover already open.
- One editor and **one human approval** instead of two of each. The cited draft is pre-filled after step 1 through the same server-checked insertion; pre-filling is not an approval. The former "I checked the transaction, sources and wording" box is removed rather than ticked by the system: the only human checkpoint for a reply is step 3 ("I checked the facts and the wording" + Approve & close · demo).
- Demo mode: opening the app with `?demo` (e.g. at the oral) never auto-opens the tour.
- Secondary features leave the main screen: a **More** menu (new test ticket, tour, keyboard shortcuts, reset) and a folded **Details** panel (account, timeline, why this result, previous tickets, policy, activity, timing, priority, export). The icon rail is replaced by Tickets / Activity / Session tabs.
- 43 interface tests (3 new: the three-step flow, the blocked-ticket card, writing your own reply). Checked at 1440 px and 375 px (no horizontal overflow). No change to the server or the guardrails.

## v0.7 · guided use · 17 November 2026

> Status: design hypothesis, retested with v0.8 (see above).

- A "Next step" bar under the ticket title always says what to do now (open the ledger, then the clearing record; compare with the verified facts; use the draft; final check; record) and what to do when no draft is possible (ask for a reference, hand over).
- A five-step guided tour on first visit (inbox, merchant question, evidence, suggested reply, you decide), restartable from "Take the tour" in the top bar; Escape or "Skip tour" closes it.
- Progressive disclosure: the suggested reply stays dimmed until both sources are opened; the reply box now sits right under the payment summary.
- Clearer labels: "Your reply to the merchant", "Record reply & close". 41 interface tests (2 new).

## v0.6 · server authority, global switch, CI · 17 November 2026

- FastAPI server (`api/index.py`, `flowassist/engine.py`) enforces the rules on insertion, final reply and handover; the browser engine stays as the instant preview. Parity test: identical results on 123 cases and 468 draft checks.
- Global assist-mode switch (`ASSIST_MODE`, fail-safe suggest-only) shown in the banner; API outage fails closed to manual handling; file:// opening is labelled "local preview".
- Local metrics: allowlisted product events and one trace per request, written to `metrics/events.jsonl` with `make dev`; `make metrics` builds the pre-launch report (docs/TRACKING_PLAN.md). No third-party analytics.
- Attack set `evals/adversarial_v0.csv` (30 rows, 0 misses), grading guideline + judge prompt + `scripts/eval/judge.py` (OpenAI `gpt-6-luna` by default, Claude optional).
- Makefile, CI on every PR, deployment gated on green CI with a production smoke test. 39 interface tests (5 new on the server path).

## v0.5 · user-test changes in the interface · 17 November 2026

- D08: the payment status reads in plain language ("Sent to recipient’s bank · not yet received", "Received by the recipient", "Returned · not received") with an amber / green / red tone, in the summary chip and the timeline. The ledger code no longer appears as a green "ready" chip. Draft wording is unchanged.
- D09: a "Verified facts" box above the suggested reply lists amount, reference, plain status, last bank event and sources checked (n of 2); it turns green once every source is inspected.
- D10: each evidence button says what the record confirms; the ledger is marked "open first".
- Payment summary moved directly under the merchant message (desktop and mobile).
- Sentence-case labels instead of tracked capitals, a shield mark instead of the sparkle, "You approve" instead of the bare "L2" tag, and a 12px floor for captions.
- Checked at 1440px and at a true 375px width (no horizontal overflow); 34 tests pass. Not a new user test: the next tests should check whether the "sent to bank" misreading is gone.

## Step 1 router and policy gaps · 17 November 2026

- Router (`classify`): money-action requests now cover reimburse, credit back, recredit, Rückerstattung/erstatten, Rückbuchung, devolución, cancel/reverse/annuler/stornieren a payment, fee waivers and compensation; a new `legal` route catches lawyer/avocat/Anwalt/court/lawsuit threats. All go to a person. "bloqué" (stuck) deliberately stays tracing.
- Policy checker (`evaluateDraft`): added critical blocks for affirmative commitments added to a draft — "we will credit back/refund/reimburse", "your refund is on its way", fee waived, compensation/entitlement claims, "will arrive / next week" and their FR/DE equivalents. Negated wording in generated drafts ("credit back … is not confirmed") still passes.
- Inbox status labels show "Legal" and "Money action".
- Two regression tests added (34 total). Development set unchanged: 50/50 expected states, 15 drafts, 0 drafts on human-only; `results_v0.json` regenerated for the new engine hash.

## S4 engine corrections and documentation · 9 November 2026

- Corrected reference extraction (FAC/RE/REF) and monetary token boundaries; reference digits and hyphens no longer become monetary amounts or negative signs.
- Model-derived matching inputs now require a finite numeric confidence in [0.95, 1]; unknown provenance fails closed, and untrusted source notes are excluded from drafting fields. All existing identity and evidence checks still apply.
- Expanded the development suite to 50 cases, with archived initial fixtures/engine, deterministic result hashes, 50 current expected states and 15 drafts. Added regression coverage for a total of 32 domain/interaction tests.
- Added S4 architecture, report, spec v2 changes, governance, review grids and a reproducible replay of the unmodified Paylio starter. These are development checks, not measured business performance.
- Updated the README and cross-document counts, commands, financial evidence boundary and deployment status. Primary `034267c` was pushed and publication snapshot `8a8a2cf` verified identical; updated HTTP delivery was later verified on 9 November (five assets, HTTP 200, matching hashes).

## v0.4 · 3 November 2026

- Replaced hardcoded replies with a separate synthetic data module and pure matching/drafting/checking engine.
- Added ten starting scenarios, ticket creation (up to 30), scoped account/history/PSD2/KYC context and policy references.
- Added merchant-confirmed reference clarification, waiting/reopen states, priorities, final human reply review/closure and recorded specialist handovers.
- Check amounts in integer minor units, unique references, scope, freshness, source schema, conflicts, status and citations. Sensitive, stale, unsupported and unsafe cases suppress generation. Gross payment and net credit are described separately.
- Added activity trail, JSON receipts/audit export, CSV timing export and session overview with manually pausable visible-tab timings. Completion, hidden tabs and other views stop time accumulation.
- Added per-tab sessionStorage persistence with schema checks, known secret-pattern redaction and memory fallback. Approval/inspection never restore from storage.
- Updated Vercel packaging for five runtime assets. Added 30 domain and interaction test scenarios using Node’s built-in runner.
- No live payment API, message sending, financial action, model evaluator or production security is implied. Browser-rendering checks remain outstanding.

## v0.3 · 3 November 2026

- Rebuilt the workspace with a compact brand rail, ticket inbox, clearer request hierarchy and a dedicated investigation panel. Added a local stylesheet without external fonts or UI dependencies.
- Added search across ticket IDs, messages, merchant scopes and source references; reply-ready/specialist filters; visible result count and empty state.
- Added a payment summary and evidence-backed timeline for the ready tracing scenario. Other tickets never display that summary. Historical snapshot times remain explicit.
- Added visible source/review/preparation progress and distinct ready, missing-reference, compliance and restricted states. Specialist panels open automatically on blocked tickets.
- Retained reply text, suggested-draft edits, handover notes/reason and manual mode separately for each ticket during the tab session. Source inspection and approval reset whenever a ticket is selected. Reload/reset clears memory.
- Added explicit confirmation before replacing a different existing reply, character count, reply copying with manual fallback and safe resumption of assisted review.
- Added keyboard help, search/next/previous shortcuts, an approved-draft insertion shortcut, skip link, focus styles, labelled controls and a layout whose small-screen reading order matches DOM order.
- Invalidate handover previews when notes/reason change. Source and note content continue to use text-only DOM insertion.
- Updated Vercel packaging for the stylesheet. Publication remains pending; no new hosted URL is claimed.
- Structural checks and 44 state assertions pass. Browser rendering, responsive appearance, real clipboard behavior and participant validation are not established by those checks.

## v0.2 · 3 November 2026

D01–D05: all-source inspection, direct missing-reference wording, snapshot timestamps in handover, compliance routing and disabled insertion in manual mode.

## v0.1 · 2 November 2026

Initial local inbox with four scripted tickets, source inspection, reviewed draft insertion and handover previews.
