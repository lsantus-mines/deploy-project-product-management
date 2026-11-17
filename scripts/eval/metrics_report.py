"""Pre-launch metrics report from the local event file.

Reads the JSONL written by the server (metrics/events.jsonl with `make dev`, or
a saved Vercel runtime-log export: lines with "type": "event" or "trace") and
writes metrics/report.md with the views of docs/TRACKING_PLAN.md:
funnel, guardrail blocks, handling time by segment, escalation, switch and
infrastructure. Usage: python scripts/eval/metrics_report.py [events.jsonl ...]
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "metrics/events.jsonl"
FUNNEL = ["ticket_opened", "source_inspected", "draft_used", "reply_recorded"]


def load(paths: list[Path]) -> tuple[list[dict], list[dict]]:
    events, traces = [], []
    for path in paths:
        for raw in path.read_text(encoding="utf-8").splitlines():
            raw = raw.strip()
            if not raw.startswith("{"):
                continue
            try:
                line = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if line.get("type") == "event":
                events.append(line)
            elif line.get("type") == "trace":
                traces.append(line)
    return events, traces


def pct(part: int, whole: int) -> str:
    return f"{part / whole:.0%}" if whole else "n/a"


def quantile(values: list[float], q: float) -> float:
    if len(values) == 1:
        return values[0]
    return statistics.quantiles(values, n=100, method="inclusive")[int(q * 100) - 1]


def seconds(ms: float) -> str:
    return f"{ms / 1000:.0f} s" if ms < 120000 else f"{ms / 60000:.1f} min"


def report(events: list[dict], traces: list[dict]) -> str:
    by_name = Counter(e["event"] for e in events)
    sessions = {e.get("session") for e in events}
    lines = [
        "# FlowAssist — pre-launch metrics (local)",
        "",
        f"{len(events)} events from {len(sessions)} sessions; {len(traces)} request traces. "
        f"Environment: {', '.join(sorted({e.get('env', '?') for e in events})) or 'n/a'}. "
        "Demo data: these are baselines of the instrumented workflow, not business results.",
        "",
        "## 1. Funnel (where value leaks)",
        "",
        "| Step | Events | vs tickets opened |",
        "|---|---:|---:|",
    ]
    opened = by_name["ticket_opened"]
    for step in FUNNEL:
        lines.append(f"| `{step}` | {by_name[step]} | {pct(by_name[step], opened)} |")

    lines += ["", "## 2. Guardrails (level 3)", "", "| Gate or code | Count |", "|---|---:|"]
    gates: Counter[str] = Counter()
    for e in events:
        if e["event"] == "ticket_opened" and e.get("state") != "draft_ready" and e.get("gate"):
            gates[f"routed to a person · {e['gate']}"] += 1
        if e["event"] == "guardrail_blocked":
            gates[f"server block · {e.get('gate')}"] += 1
        if e["event"] == "check_failed":
            for code in e.get("codes") or ["?"]:
                gates[f"refused {e.get('action')} · {code}"] += 1
    lines += [f"| {k} | {v} |" for k, v in gates.most_common()] or ["| none | 0 |"]

    lines += [
        "",
        "## 3. Handling time by segment (level 4 → 5; never the average alone)",
        "",
        "| Segment | Replies | p50 | p95 | Edited |",
        "|---|---:|---:|---:|---:|",
    ]
    replies = [e for e in events if e["event"] == "reply_recorded" and isinstance(e.get("handling_ms"), (int, float))]
    groups: dict[str, list[dict]] = defaultdict(list)
    for e in replies:
        groups["all"].append(e)
        groups[f"language {e.get('language')}"].append(e)
        groups[f"plan {e.get('plan')}"].append(e)
    for name, rows in sorted(groups.items(), key=lambda kv: (kv[0] != "all", kv[0])):
        values = [r["handling_ms"] for r in rows]
        edited = sum(1 for r in rows if r.get("edited"))
        lines.append(
            f"| {name} | {len(rows)} | {seconds(quantile(values, 0.5))} | {seconds(quantile(values, 0.95))} | {pct(edited, len(rows))} |"
        )
    if not replies:
        lines.append("| no reply recorded yet | 0 | – | – | – |")

    handovers = Counter(e.get("queue") for e in events if e["event"] == "handover_recorded")
    lines += ["", "## 4. Escalation", "", f"Handover rate: {pct(sum(handovers.values()), opened)} of tickets opened."]
    lines += [f"- {q}: {n}" for q, n in handovers.most_common()]

    first = Counter(e.get("source_kind") for e in events if e["event"] == "source_inspected" and e.get("order") == 1)
    lines += ["", "## 5. Source opened first (D10)", ""]
    lines += [f"- {kind}: {n} ({pct(n, sum(first.values()))})" for kind, n in first.most_common()] or ["- no data"]

    modes = Counter(e.get("assist_mode") for e in events if e["event"] == "ticket_opened")
    latencies = [t["ms"] for t in traces if isinstance(t.get("ms"), (int, float))]
    errors = sum(1 for t in traces if isinstance(t.get("status"), int) and t["status"] >= 500)
    lines += [
        "",
        "## 6. Switch and infrastructure (S7 layers)",
        "",
        f"- Assist mode on tickets opened: {dict(modes) or 'n/a'}",
        f"- Manual mode toggles: {by_name['manual_mode_toggled']}",
        f"- `api_unavailable` (browser could not reach the server): {by_name['api_unavailable']}",
        f"- Server latency p95: {quantile(latencies, 0.95):.1f} ms over {len(latencies)} requests; 5xx: {errors}"
        if latencies
        else "- Server traces: none in this file",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    paths = [Path(p) for p in sys.argv[1:]] or [DEFAULT]
    missing = [p for p in paths if not p.is_file()]
    if missing:
        print(f"No event file at {', '.join(map(str, missing))}. Run `make dev` and use the demo first.", file=sys.stderr)
        return 1
    events, traces = load(paths)
    text = report(events, traces)
    out = ROOT / "metrics/report.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text)
    print(text)
    print(f"Written to {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
