# Tracking plan — FlowAssist (pre-launch baseline)

What we measure before launch, where each event comes from, and which course
metric it feeds (S5 five-level stack, S7 four monitoring layers). **Everything
stays local**: no third-party analytics. The browser posts events to our own
server (`POST /api/events`); the server validates them against an allowlist and
writes JSON lines to stdout (Vercel runtime logs) and, with `make dev`, to
`metrics/events.jsonl` (git-ignored). `make metrics` builds `metrics/report.md`.
Every event carries `env` (`demo` until a pilot) and an anonymous ops session id.

**Privacy rule:** no event carries ticket, draft, note or reply text, nor any
amount or reference. Unknown event names are rejected, unknown property keys are
dropped, and only short scalar values are kept. Segments are coarse (language,
plan, rail).

## Events

| Event | Sent from | Key properties | Course metric (level / layer) |
|---|---|---|---|
| `ticket_opened` | browser | `language`, `plan`, `rail`, `state`, `gate`, `intent`, `assist_mode` | volume; draft-ready rate by segment (L2 AI system) |
| `source_inspected` | browser | `source_kind` (ledger/clearing), `order` | D10: is the ledger opened first? (L4 product) |
| `draft_used` | browser, after server `/api/check` | segment props | draft acceptance (L4 product) |
| `reply_recorded` | browser, after server `/api/check` | `handling_ms`, `sources_checked`, `edited`, `manual_review`, segment | active handling time vs the 41.2 % flip point (L4→L5); edit rate |
| `handover_recorded` | browser, after server `/api/handover` | `queue`, `reason`, segment | escalation rate (L4) |
| `manual_mode_toggled` | browser | `to`, segment | per-ticket switch use (L3 guardrails) |
| `api_unavailable` | browser | `endpoint` | infrastructure layer (S7) |
| `guardrail_blocked` | server `/api/analyze` | `gate`, `layer` (input/scope/output), `intent`, segment | guardrail layer: blocks by reason (L3) |
| `check_failed` | server `/api/check` | `action` (insert/reply), `codes`, segment | attempted unsafe insert/reply; floor = 0 harmful sent (L3) |

Server traces: one JSON line per request (`"type": "trace"`: `trace_id`, route,
status, latency, spans `analyze` / `evaluate_draft`, engine version, assist
mode), in the same file and logs. That is the S7 trace.

## Report sections (`make metrics` → `metrics/report.md`)

1. **Funnel** `ticket_opened` → `source_inspected` → `draft_used` → `reply_recorded` (where value leaks).
2. **Guardrails** tickets routed to a person by gate, server blocks, refused inserts/replies by code (stable week to week; a jump = drift).
3. **Handling time** p50/p95 of `handling_ms` overall, by `language`, by `plan`, with the edit rate (Simpson check: never the average alone).
4. **Escalation** handover rate and queues.
5. **Source opened first** (D10: is the ledger opened first?).
6. **Switch & infra** assist modes seen, manual toggles, `api_unavailable`, server p95 latency and 5xx.

## Global switch and future A/B

| Setting | Values | Use |
|---|---|---|
| `ASSIST_MODE` (env; Vercel variable in production) | `on` / `suggest_only` / `off` | global override switch (S7), enforced by the server; any other value → `suggest_only`. Change it and redeploy (~1 min). |
| A/B assignment | not implemented | future S6 test: unit, sample size and decision rule written in `06_07_experiments_operations.md` before any code. |

## Pre-launch thresholds (proposal for `05_metrics.md` / `06_07`)

| Layer | Metric | Pages someone when | Clock | Owner |
|---|---|---|---|---|
| Infrastructure | `api_unavailable`, p95 API latency (trace) | errors > 1 % for 10 min · p95 > 4 s | real time | on-call engineer |
| Model quality | weekly human sample vs judge agreement | agreement < 80 % | weekly | PM |
| Product & guardrails | `check_failed` on `reply`, drafts on human-only tickets | any human-only draft · `check_failed` spike ×2 week on week | daily | Head of Payment Ops |
| Business | p50 `handling_ms` vs manual baseline, by segment | saving < 41.2 % on eligible tickets at read date | weekly/monthly | Head of Payment Ops + CFO |
