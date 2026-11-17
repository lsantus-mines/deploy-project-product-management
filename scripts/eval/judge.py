"""LLM-as-a-judge for FlowAssist drafts (Assignment 5 §5).

Grades every draft of the development set with the guideline in
evals/judge_prompt.txt, then measures:
  - human-judge agreement against evals/v0/grader_reviews.csv (grader 1, and
    grader 2 once filled);
  - sensitivity on known-bad variants: each real draft is also graded with one
    injected defect (wrong amount, refund promise, status upgrade). Their
    correct verdict is "escalate" by construction, so a judge that says
    "sendable" there is over-accepting.

Writes evals/judge/judge_results.json and evals/judge/judge_report.md.

Provider (read from the environment or a local .env, never committed):
  JUDGE_PROVIDER=openai     (default) OPENAI_API_KEY, model JUDGE_MODEL or gpt-6-luna
  JUDGE_PROVIDER=anthropic  ANTHROPIC_API_KEY or `ant auth login`, model claude-opus-5-5
A judge from another model family than the drafter avoids self-preference;
the drafts here are rule templates, so either family is independent.

Costs money: about 60 short calls. Run `python scripts/eval/judge.py --dry-run`
first to check the inputs without calling the API.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from flowassist import engine  # noqa: E402

try:  # local secrets live in .env (git-ignored); CI passes real env vars
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
except ImportError:
    pass

PROVIDER = os.environ.get("JUDGE_PROVIDER", "openai").strip().lower()
DEFAULT_MODELS = {"openai": "gpt-6-luna", "anthropic": "claude-opus-5-5"}
if PROVIDER not in DEFAULT_MODELS:
    raise SystemExit(f"JUDGE_PROVIDER must be one of {sorted(DEFAULT_MODELS)}, not {PROVIDER!r}")
MODEL = os.environ.get("JUDGE_MODEL", "").strip() or DEFAULT_MODELS[PROVIDER]
PROMPT = (ROOT / "evals/judge_prompt.txt").read_text()
DEFECTS = {
    "wrong_amount": lambda d: re.sub(r"\d[\d,]*\.\d{2}", "9,999.00", d, count=1),
    "refund_promise": lambda d: f"{d} We will refund you next week.",
    "status_upgrade": lambda d: f"{d} The money has already been received by your supplier.",
}


class Grade(BaseModel):
    right_payment: bool
    no_invented_fact: bool
    no_promise_or_action: bool
    sendable_as_is: bool
    verdict: Literal["sendable", "needs_edit", "escalate"]
    rationale: str


def cases() -> list[dict]:
    fixtures = {f["id"]: f for f in json.loads((ROOT / "evals/v0/fixtures_v0.json").read_text())}
    results = json.loads((ROOT / "evals/v0/results_v0.json").read_text())["results"]
    items = []
    for r in results:
        if not (r["draft"] and r["policyPass"]):
            continue
        f = fixtures[r["id"]]
        analysis = engine.analyze(f["ticket"], f["data"])
        sources = "\n\n".join(f"[{s['id']}]\n{s['text']}" for s in analysis["sources"])
        items.append(
            {"id": r["id"], "variant": "real", "message": f["ticket"]["message"], "sources": sources, "draft": r["draft"], "expected": None}
        )
        for name, corrupt in DEFECTS.items():
            # Claiming receipt is only a defect when the payment is not credited.
            if name == "status_upgrade" and analysis["transaction"]["status"] == "credited":
                continue
            items.append(
                {
                    "id": r["id"],
                    "variant": name,
                    "message": f["ticket"]["message"],
                    "sources": sources,
                    "draft": corrupt(r["draft"]),
                    "expected": "escalate",
                }
            )
    return items


def human_grades() -> dict[str, dict[str, str]]:
    rows = list(csv.DictReader((ROOT / "evals/v0/grader_reviews.csv").open(newline="", encoding="utf-8")))
    return {r["case_id"]: r for r in rows}


def user_content(item: dict) -> str:
    return (
        f"<merchant_message>\n{item['message']}\n</merchant_message>\n\n"
        f"<sources>\n{item['sources']}\n</sources>\n\n<draft>\n{item['draft']}\n</draft>"
    )


def grade_openai(client, item: dict) -> tuple[Grade | None, dict]:
    response = client.responses.parse(
        model=MODEL,
        instructions=PROMPT,
        input=user_content(item),
        text_format=Grade,
        max_output_tokens=4000,
        prompt_cache_key="flowassist-judge-v1",  # the guideline prefix is shared by every call
        store=False,
    )
    details = getattr(response.usage, "input_tokens_details", None)
    usage = {
        "input": response.usage.input_tokens,
        "output": response.usage.output_tokens,
        "cache_read": getattr(details, "cached_tokens", 0) or 0,
    }
    return response.output_parsed, usage  # None on a refusal


def grade_anthropic(client, item: dict) -> tuple[Grade | None, dict]:
    response = client.beta.messages.parse(
        model=MODEL,
        max_tokens=4000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        output_config={"effort": "low"},
        system=[{"type": "text", "text": PROMPT, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_content(item)}],
        output_format=Grade,
    )
    usage = {
        "input": response.usage.input_tokens,
        "output": response.usage.output_tokens,
        "cache_read": response.usage.cache_read_input_tokens or 0,
    }
    if response.stop_reason == "refusal":
        return None, usage
    return response.parsed_output, usage


def agreement(pairs: list[tuple[bool, bool]]) -> str:
    if not pairs:
        return "n/a"
    same = sum(a == b for a, b in pairs)
    return f"{same}/{len(pairs)} = {same / len(pairs):.0%}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="build the inputs, call nothing")
    args = parser.parse_args()
    items = cases()
    real = [i for i in items if i["variant"] == "real"]
    print(f"{len(real)} real drafts, {len(items) - len(real)} known-bad variants, {PROVIDER} model {MODEL}")
    if args.dry_run:
        print(json.dumps(items[0], indent=2, ensure_ascii=False))
        return 0

    if PROVIDER == "openai":
        import openai

        if not os.environ.get("OPENAI_API_KEY"):
            print("OPENAI_API_KEY is missing: add it to .env (see .env.example).", file=sys.stderr)
            return 1
        client, grade, api_error = openai.OpenAI(), grade_openai, openai.APIStatusError
    else:
        import anthropic

        client, grade, api_error = anthropic.Anthropic(), grade_anthropic, anthropic.APIStatusError
    results, totals = [], {"input": 0, "output": 0, "cache_read": 0}
    for n, item in enumerate(items, 1):
        try:
            verdict, usage = grade(client, item)
        except api_error as error:
            print(f"{item['id']} {item['variant']}: API error {error.status_code}", file=sys.stderr)
            return 1
        for k in totals:
            totals[k] += usage[k]
        results.append({**{k: item[k] for k in ("id", "variant", "expected")}, "grade": verdict.model_dump() if verdict else None})
        print(f"[{n}/{len(items)}] {item['id']} {item['variant']}: {verdict.verdict if verdict else 'refused'}")

    humans = human_grades()
    human_judge_1, human_judge_2, human_human = [], [], []
    for r in results:
        if r["variant"] != "real" or not r["grade"]:
            continue
        judge_yes = r["grade"]["verdict"] == "sendable"
        h = humans.get(r["id"], {})
        if h.get("sendable_1") in ("yes", "no"):
            human_judge_1.append((h["sendable_1"] == "yes", judge_yes))
        if h.get("sendable_2") in ("yes", "no"):
            human_judge_2.append((h["sendable_2"] == "yes", judge_yes))
            if h.get("sendable_1") in ("yes", "no"):
                human_human.append((h["sendable_1"] == "yes", h["sendable_2"] == "yes"))
    bad = [r for r in results if r["variant"] != "real"]
    caught = sum(1 for r in bad if r["grade"] and r["grade"]["verdict"] == "escalate")
    over_accepted = [f"{r['id']}:{r['variant']}" for r in bad if r["grade"] and r["grade"]["verdict"] == "sendable"]

    (ROOT / "evals/judge/judge_results.json").write_text(json.dumps({"model": MODEL, "usage": totals, "results": results}, indent=2) + "\n")
    report = f"""# Judge report — {MODEL}

Guideline: `evals/judge/rubric.md` (judge prompt = guideline, copied). Inputs: {len(real)} drafts of the development set + {len(bad)} known-bad variants.

| Measure | Value |
|---|---|
| Human–human agreement (grader 1 vs grader 2, sendable yes/no) | {agreement(human_human)} |
| Human–judge agreement, grader 1 | {agreement(human_judge_1)} |
| Human–judge agreement, grader 2 | {agreement(human_judge_2)} |
| Known-bad variants escalated by the judge | {caught}/{len(bad)} |
| Known-bad variants the judge called sendable (over-acceptance) | {len(over_accepted)}: {", ".join(over_accepted) or "none"} |
| Tokens (input / output / cache read) | {totals["input"]} / {totals["output"]} / {totals["cache_read"]} |

Limits: the drafts are templates on a development set already examined by the team, and grader 1 also reviewed the labels. Agreement on {len(real)} cases is a small sample. Read the disagreements in `evals/judge/judge_results.json` before trusting the number; fix the guideline once, re-measure, then sample 5 % weekly.
"""
    (ROOT / "evals/judge/judge_report.md").write_text(report)
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
