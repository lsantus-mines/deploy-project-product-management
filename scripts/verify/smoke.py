"""Post-deploy smoke test: page, health, config, and one guardrail refusal.

Usage: python scripts/verify/smoke.py https://deploy-project-product-management.vercel.app
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = (ARGS[0] if ARGS else "http://127.0.0.1:8000").rstrip("/")
EXPECT = sys.argv[sys.argv.index("--expect-version") + 1] if "--expect-version" in sys.argv else None
TICKET = {
    "id": "SMOKE-1",
    "merchant": "M-ALPHA",
    "language": "EN",
    "message": "Could you trace our EUR 1,240 payment, reference INV-DEMO?",
    "receivedAt": "2026-11-02T10:01:00Z",
}


def call(path: str, body: dict | None = None) -> tuple[int, dict | str]:
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(f"{BASE}{path}", data=data, headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode()
            status = response.status
    except urllib.error.HTTPError as error:
        raw, status = error.read().decode(), error.code
    try:
        return status, json.loads(raw)
    except json.JSONDecodeError:
        return status, raw


def main() -> int:
    checks = []
    status, page = call("/")
    checks.append(("page", status == 200 and "FlowAssist" in str(page)))
    status, health = call("/api/health")
    checks.append(("health", status == 200 and isinstance(health, dict) and health.get("status") == "ok"))
    if EXPECT:
        checks.append((f"engine version {EXPECT}", isinstance(health, dict) and health.get("engine_version") == EXPECT))
    status, config = call("/api/config")
    checks.append(("config", status == 200 and isinstance(config, dict) and config.get("assist_mode") in ("on", "suggest_only", "off")))
    status, analysis = call("/api/analyze", {"ticket": TICKET})
    checks.append(("analyze", status == 200 and isinstance(analysis, dict) and analysis.get("state") == "draft_ready"))
    draft = analysis.get("draft") if isinstance(analysis, dict) else None
    text = f"{draft or 'Your payment'} We will refund you next week."
    status, verdict = call("/api/check", {"ticket": TICKET, "text": text, "action": "reply"})
    checks.append(("guardrail refuses a refund promise", status == 422))
    for name, ok in checks:
        print(f"{'ok  ' if ok else 'FAIL'} {name}")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
