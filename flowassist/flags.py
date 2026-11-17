"""Global assist-mode switch (the S7 override switch).

on            drafts can be inserted after the human checks
suggest_only  drafts are shown, never insertable (L1)
off           no draft at all: humans-only mode

Source: the ASSIST_MODE environment variable (default "on"); in production a
Vercel environment variable, changed by its owner then redeployed. Any value
other than the three modes fails safe to suggest_only.
"""

from __future__ import annotations

import os

MODES = ("on", "suggest_only", "off")


def assist_mode() -> tuple[str, str]:
    """Return (mode, source)."""
    raw = os.environ.get("ASSIST_MODE", "on").strip().lower()
    if raw in MODES:
        return raw, "env"
    return "suggest_only", "fail_safe"


def reset_cache() -> None:
    """Kept for tests: the mode is read on every request, nothing is cached."""
