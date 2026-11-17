"""The server enforces the rules even when the browser is bypassed."""

from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from api.index import app
from flowassist import flags
from tests.cases import demo_data

client = TestClient(app)
READY = next(t for t in demo_data()["tickets"] if t["key"] == "ready")


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    monkeypatch.delenv("METRICS_FILE", raising=False)
    monkeypatch.delenv("ASSIST_MODE", raising=False)
    flags.reset_cache()
    yield


def analyze(message: str | None = None, **extra):
    ticket = {**READY, **({"message": message} if message is not None else {})}
    return client.post("/api/analyze", json={"ticket": ticket, **extra})


def draft() -> str:
    return analyze().json()["draft"]


def test_health_and_config():
    assert client.get("/api/health").json()["status"] == "ok"
    config = client.get("/api/config").json()
    assert config["assist_mode"] == "on" and config["assist_mode_source"] == "env"


def test_analyze_returns_verified_draft():
    body = analyze().json()
    assert body["state"] == "draft_ready"
    assert body["transaction"] == "TX-100"
    assert [s["id"] for s in body["sources"]] == ["LED-100", "CLE-100"]


def test_client_cannot_inject_evidence():
    ticket = {**READY}
    response = client.post("/api/analyze", json={"ticket": ticket, "data": {"transactions": []}})
    assert response.status_code == 422  # unknown fields are rejected


def test_foreign_reference_returns_nothing():
    body = analyze("Where is BETA-PRIVATE?").json()
    assert body["state"] != "draft_ready" and body["sources"] == [] and body["draft"] is None


@pytest.mark.parametrize(
    "extra",
    [
        "We will credit back the amount next week.",
        "Nous vous rembourserons sous 3 jours.",
        "Your payment was definitely paid.",
        "See BETA-PRIVATE.",
    ],
)
def test_reply_with_forbidden_claim_is_refused(extra):
    response = client.post("/api/check", json={"ticket": READY, "text": f"{draft()} {extra}", "action": "reply"})
    assert response.status_code == 422
    assert response.json()["allowed"] is False


def test_canonical_reply_is_allowed():
    response = client.post("/api/check", json={"ticket": READY, "text": draft(), "action": "reply"})
    assert response.status_code == 200 and response.json()["passed"] is True


def test_edited_reply_needs_manual_review_but_is_allowed():
    response = client.post("/api/check", json={"ticket": READY, "text": f"{draft()} Thanks for your patience.", "action": "reply"})
    body = response.json()
    assert response.status_code == 200 and body["manual_review"] is True and body["passed"] is False


def test_reply_on_human_only_ticket_is_refused():
    ticket = {**READY, "message": "Please reimburse INV-DEMO"}
    response = client.post("/api/check", json={"ticket": ticket, "text": "Done.", "action": "reply"})
    assert response.status_code == 422 and "no_transaction" in response.json()["codes"]


@pytest.mark.parametrize("mode", ["suggest_only", "off"])
def test_global_switch_blocks_insertion(monkeypatch, mode):
    text = draft()
    monkeypatch.setenv("ASSIST_MODE", mode)
    flags.reset_cache()
    response = client.post("/api/check", json={"ticket": READY, "text": text, "action": "insert"})
    assert response.status_code == 409


def test_switch_off_withholds_drafts(monkeypatch):
    monkeypatch.setenv("ASSIST_MODE", "off")
    body = analyze().json()
    assert body["assist_mode"] == "off" and body["draft"] is None and body["state"] == "draft_ready"


def test_unknown_mode_fails_safe(monkeypatch):
    monkeypatch.setenv("ASSIST_MODE", "yolo")
    config = client.get("/api/config").json()
    assert config["assist_mode"] == "suggest_only" and config["assist_mode_source"] == "fail_safe"


def test_events_are_kept_locally_without_free_text(monkeypatch, tmp_path):
    target = tmp_path / "events.jsonl"
    monkeypatch.setenv("METRICS_FILE", str(target))
    ok = client.post(
        "/api/events",
        headers={"x-session-id": "ops-test"},
        json={
            "event": "reply_recorded",
            "properties": {"handling_ms": 61000, "language": "FR", "message": "secret ticket text", "gate": "x" * 200},
        },
    )
    assert ok.status_code == 202
    line = json.loads(target.read_text().splitlines()[0])
    assert line["event"] == "reply_recorded" and line["handling_ms"] == 61000 and line["language"] == "FR"
    assert "message" not in line and "gate" not in line  # unknown key and over-long text are dropped
    assert client.post("/api/events", json={"event": "export_all_tickets"}).status_code == 422


def test_refused_reply_is_recorded_as_check_failed(monkeypatch, tmp_path):
    target = tmp_path / "events.jsonl"
    monkeypatch.setenv("METRICS_FILE", str(target))
    client.post("/api/check", json={"ticket": READY, "text": f"{draft()} We will refund you next week.", "action": "reply"})
    lines = [json.loads(x) for x in target.read_text().splitlines()]
    events = [x for x in lines if x["type"] == "event"]
    assert [e["event"] for e in events] == ["check_failed"] and events[0]["codes"] == ["commitment"]
    assert any(x["type"] == "trace" and x["route"] == "check" and x["status"] == 422 for x in lines)


def test_handover_requires_reason_and_redacts_note():
    bad = client.post("/api/handover", json={"ticket": READY, "reason": " ", "note": ""})
    assert bad.status_code == 422
    good = client.post("/api/handover", json={"ticket": READY, "reason": "Merchant asked for a person", "note": "password: hunter2"})
    packet = good.json()["packet"]
    assert "hunter2" not in packet["note"] and packet["queue"] == "Tier-2 payments"


def test_oversized_message_is_rejected():
    assert analyze("x" * 3001).status_code == 422
