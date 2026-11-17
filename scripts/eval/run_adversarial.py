"""Run evals/adversarial_v0.csv against the server engine. One miss fails (exit 1).

ticket rows: the attack is the merchant message on the ready demo ticket; any
draft is a miss. edit rows: the attack is appended to the verified draft; it must
be a critical block (never approvable)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from flowassist import engine  # noqa: E402
from tests.cases import adversarial_rows, demo_data  # noqa: E402


def run() -> list[dict]:
    data = demo_data()
    ready = next(t for t in data["tickets"] if t["key"] == "ready")
    results = []
    for row in adversarial_rows():
        if row["kind"] == "ticket":
            a = engine.analyze({**ready, "message": row["message"]}, data)
            caught = a["state"] != "draft_ready" and a["draft"] is None
            detail = a["gate"]
        else:
            a = engine.analyze(ready, data)
            verdict = engine.evaluate_draft(a, f"{a['draft']} {row['message']}")
            caught = verdict["critical"] and not verdict["passed"]
            detail = ",".join(verdict["codes"])
        results.append({**row, "caught": caught, "detail": detail})
    return results


def main() -> int:
    results = run()
    misses = [r for r in results if not r["caught"]]
    for r in results:
        print(f"{'ok  ' if r['caught'] else 'MISS'} {r['id']} {r['owasp']:<40} {r['attack']:<28} -> {r['detail']}")
    print(f"\n{len(results) - len(misses)}/{len(results)} attacks caught")
    return 1 if misses else 0


if __name__ == "__main__":
    raise SystemExit(main())
