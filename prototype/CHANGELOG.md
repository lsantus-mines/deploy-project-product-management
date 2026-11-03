# FlowAssist interface changelog

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
