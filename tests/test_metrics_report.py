import json

from scripts.eval.metrics_report import load, report


def test_report_covers_the_tracking_plan_views(tmp_path):
    rows = [
        {"type": "event", "event": "ticket_opened", "session": "a", "env": "demo", "state": "draft_ready", "assist_mode": "on"},
        {
            "type": "event",
            "event": "ticket_opened",
            "session": "a",
            "env": "demo",
            "state": "human_only",
            "gate": "Dispute specialist required",
        },
        {"type": "event", "event": "source_inspected", "session": "a", "env": "demo", "source_kind": "ledger", "order": 1},
        {"type": "event", "event": "draft_used", "session": "a", "env": "demo"},
        {
            "type": "event",
            "event": "reply_recorded",
            "session": "a",
            "env": "demo",
            "handling_ms": 90000,
            "language": "FR",
            "plan": "Enterprise",
            "edited": True,
        },
        {"type": "event", "event": "check_failed", "session": "a", "env": "demo", "action": "reply", "codes": ["commitment"]},
        {"type": "event", "event": "handover_recorded", "session": "a", "env": "demo", "queue": "Tier-2 disputes"},
        {"type": "trace", "route": "check", "status": 422, "ms": 1.5},
    ]
    path = tmp_path / "events.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\nnot json\n")
    text = report(*load([path]))
    assert "| `reply_recorded` | 1 | 50% |" in text
    assert "routed to a person · Dispute specialist required | 1" in text
    assert "refused reply · commitment | 1" in text
    assert "| language FR | 1 | 90 s | 90 s | 100% |" in text
    assert "Tier-2 disputes: 1" in text and "ledger: 1 (100%)" in text
