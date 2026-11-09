# FlowAssist interface changelog

## S4 engine corrections and documentation · 9 November 2026

- Corrected reference extraction (FAC/RE/REF) and monetary token boundaries; reference digits and hyphens no longer become monetary amounts or negative signs.
- Model-derived matching inputs now require a finite numeric confidence in [0.95, 1]; unknown provenance fails closed, and untrusted source notes are excluded from drafting fields. All existing identity and evidence checks still apply.
- Expanded the development suite to 50 cases, with archived initial fixtures/engine, deterministic result hashes, 50 current expected states and 15 drafts. Added regression coverage for a total of 32 domain/interaction tests.
- Added S4 architecture, report, spec v2 changes, governance, review grids and a reproducible replay of the unmodified Paylio starter. These are development checks, not measured business performance.
- Updated the README and cross-document counts, commands, financial evidence boundary and deployment status. Primary `034267c` was pushed and publication snapshot `8a8a2cf` verified identical; updated HTTP delivery remains unconfirmed after DNS failure.

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
