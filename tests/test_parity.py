"""The browser preview (prototype/engine.js) and the server authority
(flowassist/engine.py) must agree on every case, or the UI would show one
verdict and the server enforce another."""

from __future__ import annotations

import copy
import json
import subprocess
from pathlib import Path

import pytest

from flowassist import engine
from tests.cases import adversarial_rows, demo_data, draft_probes, router_probes

ROOT = Path(__file__).resolve().parents[1]


def build_cases() -> list[dict]:
    cases: list[dict] = []
    for fixture in json.loads((ROOT / "evals/v0/fixtures_v0.json").read_text()):
        cases.append({"name": fixture["id"], "ticket": fixture["ticket"], "data": fixture["data"]})
    data = demo_data()
    for ticket in data["tickets"]:
        cases.append({"name": f"demo:{ticket['key']}", "ticket": ticket, "data": data})
    ambiguous = next(t for t in data["tickets"] if t["key"] == "ambiguous")
    for reference in ("INV-A", "INV-B", "BETA-PRIVATE", " inv-a "):
        cases.append({"name": f"ref:{reference}", "ticket": ambiguous, "data": data, "reference": reference})
    ready = next(t for t in data["tickets"] if t["key"] == "ready")
    for i, message in enumerate(router_probes()):
        cases.append({"name": f"probe:{i}", "ticket": {**ready, "message": message}, "data": data})
    for row in adversarial_rows():
        cases.append({"name": f"adv:{row['id']}", "ticket": {**ready, "message": row["message"]}, "data": data})
    for case in cases:
        case.setdefault("texts", [])
    return cases


def run_js(cases: list[dict]) -> list[dict]:
    payload = [{k: v for k, v in c.items() if not k.startswith("_") and k != "name"} for c in cases]
    result = subprocess.run(
        ["node", str(ROOT / "scripts/eval/js_engine_runner.cjs")],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def run_py(case: dict) -> dict:
    a = engine.analyze(copy.deepcopy(case["ticket"]), copy.deepcopy(case["data"]), case.get("reference", ""))
    return {
        "state": a["state"],
        "gate": a["gate"],
        "intent": a["intent"],
        "queue": a["queue"],
        "reason": a["reason"],
        "draft": a["draft"],
        "transaction": a["transaction"]["id"] if a["transaction"] else None,
        "sources": [[s["id"], s["text"]] for s in a["sources"]],
        "candidates": [t["id"] for t in a["candidates"]],
        "checks": a["checks"],
        "evaluations": [
            {k: r[k] for k in ("passed", "critical", "issues")} for r in (engine.evaluate_draft(a, t) for t in case.get("texts", []))
        ],
    }


def with_draft_texts(cases: list[dict]) -> list[dict]:
    """Second pass: once the JS engine has produced drafts, probe each one."""
    first = run_js(cases)
    for case, js in zip(cases, first, strict=True):
        if js["draft"]:
            case["texts"] = [js["draft"], *[f"{js['draft']} {extra}" for extra in draft_probes()], "", "Your payment was definitely paid."]
    return cases


CASES = with_draft_texts(build_cases())
JS_RESULTS = run_js(CASES)


def test_case_count() -> None:
    assert len(CASES) >= 60


@pytest.mark.parametrize("index", range(len(CASES)), ids=[c["name"] for c in CASES])
def test_python_matches_javascript(index: int) -> None:
    assert run_py(CASES[index]) == JS_RESULTS[index]
