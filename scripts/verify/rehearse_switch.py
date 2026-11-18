"""Local rehearsal of the global switch (S7 rollback plan).

Restarts the API once per mode, which stands in for the Vercel redeploy, and
records what the server does with a synthetic ticket. Run from the repo root:

    .venv/bin/python scripts/verify/rehearse_switch.py

This is a local check by one operator. It does not replace the staging
rehearsal with the two people who can press the switch.
"""

from __future__ import annotations

import datetime
import os
import subprocess
import sys
import time

import httpx

sys.path.insert(0, os.getcwd())
from tests.cases import demo_data  # noqa: E402

READY = next(t for t in demo_data()["tickets"] if t["key"] == "ready")
PORT = "8765"
URL = f"http://127.0.0.1:{PORT}"


def main() -> None:
    commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    print(f"FlowAssist switch rehearsal · {datetime.datetime.now().astimezone():%Y-%m-%d %H:%M %Z} · commit {commit}")
    print("Local uvicorn restart per mode stands in for the Vercel redeploy. Synthetic ticket 'ready'.\n")
    print(f"{'mode set':<14}{'restart→healthy':>16}  {'/api/config':<26}{'analyze: draft?':<17}{'insert draft':>13}")
    for mode in ["on", "suggest_only", "off", "on"]:
        start = time.monotonic()
        server = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "api.index:app", "--port", PORT],
            env={**os.environ, "ASSIST_MODE": mode},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            while True:
                try:
                    if httpx.get(URL + "/api/health").status_code == 200:
                        break
                except httpx.HTTPError:
                    time.sleep(0.1)
            up = time.monotonic() - start
            config = httpx.get(URL + "/api/config").json()
            analysis = httpx.post(URL + "/api/analyze", json={"ticket": READY}).json()
            text = analysis["draft"] or "Manual reply."
            insert = httpx.post(URL + "/api/check", json={"ticket": READY, "text": text, "action": "insert"}).status_code
            source = f"{config['assist_mode']} ({config['assist_mode_source']})"
            drafted = "yes" if analysis["draft"] else "no (withheld)"
            print(f"{mode:<14}{up:>14.1f} s  {source:<26}{drafted:<17}{insert:>13}")
        finally:
            server.terminate()
            server.wait()


if __name__ == "__main__":
    main()
