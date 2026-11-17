"""Traces and product events, kept locally. Never stores ticket, draft or note text.

- One JSON trace line per request (`"type": "trace"`): route, status, latency,
  spans. On Vercel these are the runtime logs; locally they also go to METRICS_FILE.
- Product events (`"type": "event"`) from the browser (POST /api/events) and
  from the server (guardrail decisions). They are printed on stdout and, when
  METRICS_FILE is set (`make dev` sets metrics/events.jsonl), appended to that
  JSONL file. `make metrics` turns the file into the pre-launch report.

Events are validated against an allowlist of names and property keys, and only
short scalar values are kept, so free text cannot leak into the metrics.
"""

from __future__ import annotations

import json
import os
import sys
import threading
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

EVENTS = {
    "ticket_opened",
    "source_inspected",
    "draft_used",
    "reply_recorded",
    "handover_recorded",
    "manual_mode_toggled",
    "api_unavailable",
    "guardrail_blocked",
    "check_failed",
}
PROPERTIES = {
    "language",
    "plan",
    "rail",
    "state",
    "gate",
    "intent",
    "layer",
    "assist_mode",
    "source_kind",
    "order",
    "handling_ms",
    "sources_checked",
    "edited",
    "manual_review",
    "queue",
    "reason",
    "to",
    "endpoint",
    "route",
    "action",
    "codes",
}
_lock = threading.Lock()


def clean(properties: dict[str, Any]) -> dict[str, Any]:
    """Keep allowlisted keys with short scalar values (or lists of short strings)."""
    kept: dict[str, Any] = {}
    for key, value in properties.items():
        if key not in PROPERTIES:
            continue
        if isinstance(value, bool) or value is None or (isinstance(value, (int, float)) and abs(value) < 1e12):
            kept[key] = value
        elif isinstance(value, str) and len(value) <= 80:
            kept[key] = value
        elif isinstance(value, list) and all(isinstance(v, str) and len(v) <= 40 for v in value[:10]):
            kept[key] = value[:10]
    return kept


def record_event(event: str, session: str, properties: dict[str, Any], source: str = "server") -> dict[str, Any] | None:
    if event not in EVENTS:
        return None
    line = {
        "type": "event",
        "at": datetime.now(UTC).isoformat(timespec="milliseconds"),
        "event": event,
        "session": session[:80],
        "source": source,
        "env": os.environ.get("FLOWASSIST_ENV", "demo"),
        **clean(properties),
    }
    _write(line)
    return line


def _write(line: dict[str, Any]) -> None:
    """stdout always (Vercel runtime logs); METRICS_FILE too when set (local)."""
    text = json.dumps(line, ensure_ascii=False)
    print(text, file=sys.stdout, flush=True)
    target = os.environ.get("METRICS_FILE", "").strip()
    if target:
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        with _lock, path.open("a", encoding="utf-8") as f:
            f.write(text + "\n")


class Trace:
    def __init__(self, route: str) -> None:
        self.trace_id = uuid.uuid4().hex
        self.route = route
        self.started = time.perf_counter()
        self.spans: list[dict[str, Any]] = []
        self.attributes: dict[str, Any] = {}

    @contextmanager
    def span(self, name: str, **attributes: Any) -> Iterator[dict[str, Any]]:
        record: dict[str, Any] = {"name": name, **attributes}
        start = time.perf_counter()
        try:
            yield record
        finally:
            record["ms"] = round((time.perf_counter() - start) * 1000, 2)
            self.spans.append(record)

    def emit(self, status: int) -> None:
        line = {
            "type": "trace",
            "trace_id": self.trace_id,
            "route": self.route,
            "status": status,
            "ms": round((time.perf_counter() - self.started) * 1000, 2),
            **self.attributes,
            "spans": self.spans,
        }
        _write(line)
