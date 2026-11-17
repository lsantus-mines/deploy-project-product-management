"""FlowAssist API — the server-side authority for every recorded action.

The browser shows an instant preview with prototype/engine.js; these endpoints
decide. Evidence comes only from server fixtures (flowassist/fixtures.json),
never from the request, so a client cannot inject transactions or sources.

GET  /api/health    liveness + engine version
GET  /api/config    assist mode (global switch)
POST /api/analyze   verdict, authorized sources and draft for one ticket
POST /api/check     server guardrail on a draft insertion or a final reply
POST /api/handover  validated, redacted specialist handover packet
POST /api/events    product events from the browser (allowlisted, no text)
"""

from __future__ import annotations

import json
import os
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from flowassist import engine, flags, telemetry  # noqa: E402

app = FastAPI(title="FlowAssist API", version=engine.ENGINE_VERSION, docs_url="/api/docs", openapi_url="/api/openapi.json")


@lru_cache(maxsize=1)
def server_data() -> dict[str, Any]:
    return json.loads((Path(__file__).resolve().parents[1] / "flowassist/fixtures.json").read_text())


class Ticket(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(max_length=40)
    merchant: str = Field(max_length=40)
    language: str = Field(max_length=8)
    message: str = Field(max_length=3000)
    receivedAt: str = Field(max_length=40)
    sensitiveInput: bool = False


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ticket: Ticket
    reference: str = Field(default="", max_length=60)


class CheckRequest(AnalyzeRequest):
    text: str = Field(max_length=4000)
    action: Literal["insert", "reply"]


class HandoverRequest(AnalyzeRequest):
    reason: str = Field(max_length=120)
    note: str = Field(default="", max_length=1000)


def segment(ticket: Ticket, analysis: dict[str, Any]) -> dict[str, Any]:
    account = analysis.get("account") or {}
    tx = analysis.get("transaction") or {}
    return {
        "language": ticket.language,
        "plan": account.get("plan"),
        "rail": tx.get("rail"),
        "merchant": ticket.merchant,
    }


def run_analysis(body: AnalyzeRequest, trace: telemetry.Trace) -> dict[str, Any]:
    with trace.span("analyze") as span:
        analysis = engine.analyze(body.ticket.model_dump(), server_data(), body.reference)
        span.update(state=analysis["state"], intent=analysis["intent"], layer=analysis.get("layer"))
    trace.attributes.update(ticket=body.ticket.id, engine_version=engine.ENGINE_VERSION, **segment(body.ticket, analysis))
    return analysis


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {"status": "ok", "engine_version": engine.ENGINE_VERSION}


@app.get("/api/config")
def config() -> dict[str, Any]:
    mode, source = flags.assist_mode()
    return {
        "assist_mode": mode,
        "assist_mode_source": source,
        "engine_version": engine.ENGINE_VERSION,
        "env": os.environ.get("FLOWASSIST_ENV", "demo"),
    }


@app.post("/api/analyze")
def analyze(body: AnalyzeRequest, x_session_id: str = Header(default="anonymous", max_length=80)) -> dict[str, Any]:
    trace = telemetry.Trace("analyze")
    analysis = run_analysis(body, trace)
    mode, _ = flags.assist_mode()
    draft = analysis["draft"] if mode != "off" else None
    if analysis["state"] != "draft_ready":
        telemetry.record_event(
            "guardrail_blocked",
            x_session_id,
            {
                "route": "analyze",
                "gate": analysis["gate"],
                "layer": analysis.get("layer"),
                "intent": analysis["intent"],
                **segment(body.ticket, analysis),
            },
        )
    trace.attributes["assist_mode"] = mode
    trace.emit(200)
    return {
        "state": analysis["state"],
        "gate": analysis["gate"],
        "reason": analysis["reason"],
        "queue": analysis["queue"],
        "intent": analysis["intent"],
        "checks": analysis["checks"],
        "transaction": (analysis["transaction"] or {}).get("id"),
        "sources": [{"id": s["id"], "fetchedAt": s["fetchedAt"], "text": s["text"]} for s in analysis["sources"]],
        "draft": draft,
        "assist_mode": mode,
        "engine_version": engine.ENGINE_VERSION,
    }


@app.post("/api/check")
def check(body: CheckRequest, x_session_id: str = Header(default="anonymous", max_length=80)) -> JSONResponse:
    trace = telemetry.Trace("check")
    analysis = run_analysis(body, trace)
    mode, _ = flags.assist_mode()
    if body.action == "insert" and mode != "on":
        trace.emit(409)
        return JSONResponse(
            status_code=409,
            content={
                "allowed": False,
                "codes": ["assist_mode"],
                "issues": [f"Assisted insertion is disabled (assist mode: {mode})."],
                "assist_mode": mode,
            },
        )
    with trace.span("evaluate_draft") as span:
        verdict = engine.evaluate_draft(analysis, body.text)
        span.update(codes=verdict["codes"], critical=verdict["critical"])
    payload = {
        "allowed": not verdict["critical"],
        "passed": verdict["passed"],
        "manual_review": verdict["codes"] == ["manual_review"],
        "codes": verdict["codes"],
        "issues": verdict["issues"],
        "assist_mode": mode,
    }
    status = 422 if verdict["critical"] else 200
    if verdict["critical"]:
        telemetry.record_event(
            "check_failed", x_session_id, {"action": body.action, "codes": verdict["codes"], **segment(body.ticket, analysis)}
        )
    trace.emit(status)
    return JSONResponse(status_code=status, content=payload)


@app.post("/api/handover")
def handover(body: HandoverRequest) -> JSONResponse:
    trace = telemetry.Trace("handover")
    analysis = run_analysis(body, trace)
    try:
        packet = engine.handover(body.ticket.model_dump(), analysis, body.reason, body.note)
    except ValueError as error:
        trace.emit(422)
        return JSONResponse(status_code=422, content={"allowed": False, "issues": [str(error)]})
    trace.emit(200)
    return JSONResponse(content={"allowed": True, "packet": packet})


class EventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event: str = Field(max_length=40)
    properties: dict[str, Any] = Field(default_factory=dict)


@app.post("/api/events", status_code=202)
def events(body: EventRequest, x_session_id: str = Header(default="anonymous", max_length=80)) -> JSONResponse:
    if len(body.properties) > 20:
        return JSONResponse(status_code=422, content={"accepted": False, "issues": ["Too many properties."]})
    line = telemetry.record_event(body.event, x_session_id, body.properties, source="browser")
    if line is None:
        return JSONResponse(status_code=422, content={"accepted": False, "issues": [f"Unknown event: {body.event}"]})
    return JSONResponse(status_code=202, content={"accepted": True})


# Local development only (`make dev`): serve the prototype from the same origin
# so the browser reaches /api without CORS. Vercel serves dist/ itself.
if os.environ.get("FLOWASSIST_SERVE_STATIC") == "1":
    from fastapi.staticfiles import StaticFiles

    app.mount("/", StaticFiles(directory=Path(__file__).resolve().parents[1] / "prototype", html=True), name="prototype")
