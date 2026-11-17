"""Server-side FlowAssist engine: the authority for every recorded action.

Port of prototype/engine.js. The browser copy gives an instant preview; this
module decides. tests/test_parity.py runs both on the same cases and requires
identical states, gates, drafts and policy verdicts, so the two cannot drift.

Deterministic rules and templates only: no model, bank or ticketing call.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import UTC, datetime
from typing import Any

ENGINE_VERSION = "0.6.0"
SAFE_MAX = 2**53 - 1  # JavaScript Number.MAX_SAFE_INTEGER


# ── formatting ──────────────────────────────────────────────────────────────
def money(minor: int, currency: str) -> str:
    return f"{currency} {minor / 100:,.2f}"


def _parse_date(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _ms(value: Any) -> float | None:
    parsed = _parse_date(value)
    return parsed.timestamp() * 1000 if parsed else None


def stamp(value: Any) -> str:
    parsed = _parse_date(value)
    if not parsed:
        return "Timestamp unavailable"
    utc = datetime.fromtimestamp(parsed.timestamp(), UTC)
    return utc.strftime("%Y-%m-%d %H:%M") + " UTC"


def normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    return re.sub("[̀-ͯ]", "", decomposed).lower()


# ── input guardrails ────────────────────────────────────────────────────────
def parse_minor(value: str) -> int | None:
    cleaned = re.sub(r"\s", "", str(value))
    if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d{1,2})?", cleaned, re.ASCII):
        cleaned = cleaned.replace(",", "")
    elif re.fullmatch(r"\d+(,\d{1,2})", cleaned, re.ASCII):
        cleaned = cleaned.replace(",", ".", 1)
    if not re.fullmatch(r"\d+(\.\d{1,2})?", cleaned, re.ASCII):
        return None
    whole, _, fraction = cleaned.partition(".")
    minor = int(whole) * 100 + int(fraction.ljust(2, "0") or "0")
    return minor if 0 < minor <= SAFE_MAX else None


AMOUNT_RE = re.compile(
    r"(?:\b(EUR|USD)\s*|([€$])\s*)(\d[\d\s,.]*\d|\d)|(?<![A-Za-z0-9-])(\d[\d\s,.]*\d|\d)\s*(EUR|USD|euros?)\b",
    re.IGNORECASE | re.ASCII,
)
REFERENCE_RE = re.compile(r"\b(?:INV|FAC|RE|REF|TX|SWIFT|RETURN|NET|STALE|CHECK|BETA)-[A-Z0-9-]+\b", re.ASCII)


def entities(text: str) -> dict[str, Any]:
    amounts: list[dict[str, Any]] = []
    invalid = False
    for m in AMOUNT_RE.finditer(text):
        minor = parse_minor((m.group(3) or m.group(4)).strip())
        token = (m.group(1) or m.group(2) or m.group(5)).upper()
        if minor is not None:
            amounts.append({"minor": minor, "currency": "USD" if token in ("$", "USD") else "EUR"})
        else:
            invalid = True
    references = list(dict.fromkeys(REFERENCE_RE.findall(text.upper())))
    return {"amounts": amounts, "references": references, "invalidAmount": invalid}


SECRET_RE = re.compile(
    r"(password|mot de passe|passwort|api[_ -]?key)\s*[:=]\s*[^\s,;]+|\bsk_live_[A-Za-z0-9_]+|\bFAKE_SECRET[A-Za-z0-9_]*|\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]){11,30}\b",
    re.IGNORECASE | re.ASCII,
)


def sanitize_input(value: str) -> dict[str, Any]:
    safe, count = SECRET_RE.subn("[REDACTED_SECRET]", str(value))
    return {"text": safe, "flagged": count > 0 or "[REDACTED_SECRET]" in safe}


# Step 1 · router (rung 1). Only plain tracing may reach drafting; the most
# sensitive route wins. Same lists as prototype/engine.js ROUTES.
ROUTES: list[tuple[str, re.Pattern[str]]] = [
    (
        "compliance",
        re.compile(
            r"\b(kyc|aml|compliance|fraud|fraude|betrug|sanction|sanktion)\b|freigeben|geben sie sie frei|frozen|hold.{0,20}release|release.{0,20}hold",
            re.ASCII,
        ),
    ),
    ("dispute", re.compile(r"chargeback|disput|contestation|litige|reklamation|widerspruch", re.ASCII)),
    (
        "legal",
        re.compile(
            r"\b(lawyer|attorney|solicitor|lawsuit|sue|suing|legal action|court|avocat|tribunal|mise en demeure|poursuite|anwalt|rechtsanwalt|klage|gericht|abogado|demanda)\b",
            re.ASCII,
        ),
    ),
    (
        "money_action",
        re.compile(
            r"refund|rembours|reimburs|reembols|devolu|erstatt|ruckbuch|credit.{0,12}back|recredit|release.{0,15}fund|transfer.{0,10}now|execute.{0,10}payment|\b(cancel|annul|storn|revers|recall|stop)\w*.{0,25}(payment|transfer|virement|paiement|zahlung|uberweisung|it|le|la|sie)\b|\b(waive|waiver|compensat|indemni|entschadig|geste commercial|kulanz|goodwill)\w*",
            re.ASCII,
        ),
    ),
]


def classify(text: str) -> str:
    n = normalize(text)
    for intent, pattern in ROUTES:
        if pattern.search(n):
            return intent
    return "tracing"


INJECTION_RE = re.compile(
    r"ignore.{0,30}(session|scope|tenant)|admin override|system:|reveal.{0,20}other merchant",
    re.IGNORECASE | re.ASCII,
)
UNSUPPORTED_MONEY_RE = re.compile(
    r"\b(?:GBP|JPY|CHF|CAD)\b|[£¥]|(?:EUR|USD|€|\$)\s*[-−]|(?:^|\s)[-−]\s*\d[\d ,.]*\s*(?:EUR|USD)",
    re.IGNORECASE | re.ASCII,
)


# ── drafting ────────────────────────────────────────────────────────────────
def source_records(tx: dict[str, Any]) -> list[dict[str, Any]]:
    fee = (
        f"Documented fee: {money(tx['feeMinor'], tx['currency'])} · net: {money(tx['netMinor'], tx['currency'])}\n"
        if tx.get("feeMinor")
        else ""
    )
    unconfirmed = "Beneficiary credit: NOT confirmed\n" if tx["status"] == "sent_to_bank" else ""
    return [
        {
            "id": tx["ledger"],
            "merchant": tx["merchant"],
            "transaction": tx["id"],
            "fetchedAt": tx["fetchedAt"],
            "text": f"{tx['merchant']} · {tx['id']} · {tx['reference']}\n{money(tx['amountMinor'], tx['currency'])} · {tx['status']}\n{fee}Fetched: {stamp(tx['fetchedAt'])}",
        },
        {
            "id": tx["clearing"],
            "merchant": tx["merchant"],
            "transaction": tx["id"],
            "fetchedAt": tx["fetchedAt"],
            "text": f"{tx['merchant']} · {tx['id']} · {tx.get('rail')}\nStatus: {tx.get('clearingStatus') or tx['status']}\nEvent: {stamp(tx['eventAt'])}\n{unconfirmed}Fetched: {stamp(tx['fetchedAt'])}",
        },
    ]


def make_draft(ticket: dict[str, Any], tx: dict[str, Any]) -> str:
    amount = money(tx["amountMinor"], tx["currency"])
    date = stamp(tx["eventAt"])
    citations = f"[{tx['ledger']}; {tx['clearing']}]"
    lang = ticket.get("language")
    en = {
        "pending": f"is pending as of {date}. No beneficiary credit is confirmed.",
        "sent_to_bank": f"was sent to the bank on {date}. Beneficiary credit is not yet confirmed.",
        "credited": f"was credited on {date}.",
        "failed": f"failed on {date}. The available records do not specify a reason or a refund date.",
        "returned": f"was returned on {date}. A credit back to your account is not confirmed.",
    }
    fr = {
        "pending": f"est en attente au {date}. Le crédit au bénéficiaire n’est pas confirmé.",
        "sent_to_bank": f"a été transmis à la banque le {date}. Le crédit au bénéficiaire n’est pas confirmé.",
        "credited": f"a été crédité le {date}.",
        "failed": f"a échoué le {date}. Les sources ne précisent ni motif ni date de remboursement.",
        "returned": f"a été retourné le {date}. Le recrédit de votre compte n’est pas confirmé.",
    }
    de = {
        "pending": f"ist zum {date} ausstehend. Eine Gutschrift beim Empfänger ist nicht bestätigt.",
        "sent_to_bank": f"wurde am {date} an die Bank übermittelt. Eine Gutschrift beim Empfänger ist nicht bestätigt.",
        "credited": f"wurde am {date} gutgeschrieben.",
        "failed": f"ist am {date} fehlgeschlagen. Die Unterlagen nennen weder einen Grund noch einen Erstattungstermin.",
        "returned": f"wurde am {date} zurückgegeben. Eine Kontogutschrift ist nicht bestätigt.",
    }
    prefix = "Votre paiement" if lang == "FR" else "Ihre Zahlung" if lang == "DE" else "Your payment"
    if tx.get("feeMinor") and tx["status"] == "credited":
        fee = money(tx["feeMinor"], tx["currency"])
        net = money(tx["netMinor"], tx["currency"])
        ref = f"({tx['reference']}, {tx['id']})"
        if lang == "FR":
            return f"Votre paiement brut {amount} {ref} comporte des frais documentés de {fee}. Le montant net {net} a été crédité le {date}. {citations}"
        if lang == "DE":
            return f"Ihre Bruttozahlung {amount} {ref} hat eine dokumentierte Gebühr von {fee}. Der Nettobetrag {net} wurde am {date} gutgeschrieben. {citations}"
        return f"Your gross payment {amount} {ref} has a documented fee of {fee}. The net amount {net} was credited on {date}. {citations}"
    table = fr if lang == "FR" else de if lang == "DE" else en
    reply = f"{prefix} {amount} ({tx['reference']}, {tx['id']}) {table[tx['status']]} {citations}"
    if tx.get("feeMinor"):
        fee = money(tx["feeMinor"], tx["currency"])
        net = money(tx["netMinor"], tx["currency"])
        if lang == "FR":
            reply += f" Montant brut {amount}, frais documentés {fee}, montant net documenté {net}. {citations}"
        elif lang == "DE":
            reply += f" Bruttobetrag {amount}, dokumentierte Gebühr {fee}, dokumentierter Nettobetrag {net}. {citations}"
        else:
            reply += f" Gross amount {amount}, documented fee {fee}, documented net amount {net}. {citations}"
    return reply


# ── analysis: scope, matching, evidence ─────────────────────────────────────
STATUSES = ("pending", "sent_to_bank", "credited", "failed", "returned")


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _safe_int(value: Any) -> bool:
    return _is_number(value) and float(value).is_integer() and abs(value) <= SAFE_MAX


def _bad_source(tx: dict[str, Any]) -> bool:
    return (
        not _safe_int(tx.get("amountMinor"))
        or tx["amountMinor"] <= 0
        or tx.get("currency") not in ("EUR", "USD")
        or tx.get("status") not in STATUSES
        or not tx.get("fetchedAt")
        or not tx.get("eventAt")
        or _ms(tx.get("fetchedAt")) is None
        or _ms(tx.get("eventAt")) is None
        or not re.fullmatch(r"LED-[A-Z0-9-]+", str(tx.get("ledger")))
        or not re.fullmatch(r"CLE-[A-Z0-9-]+", str(tx.get("clearing")))
    )


def analyze(ticket: dict[str, Any], data: dict[str, Any], confirmed_reference: str = "") -> dict[str, Any]:
    message = ticket.get("message", "")
    account = next((a for a in data["accounts"] if a["id"] == ticket.get("merchant")), None)
    extracted = entities(message)
    intent = classify(message)
    base: dict[str, Any] = {
        "account": account,
        "intent": intent,
        "entities": extracted,
        "candidates": [],
        "sources": [],
        "transaction": None,
        "draft": None,
        "state": "context_only",
        "queue": "Tier-2 payments",
        "checks": [],
        "reason": "",
        "gate": "",
    }

    def block(gate: str, reason: str, state: str = "context_only", queue: str = "Tier-2 payments", layer: str = "scope") -> dict[str, Any]:
        return {**base, "gate": gate, "reason": reason, "state": state, "queue": queue, "layer": layer}

    if not account:
        return block("Merchant scope unavailable", "No account context or transaction evidence is available.", "human_only")
    if ticket.get("language") not in ("EN", "FR", "DE"):
        return block("Language specialist needed", "This language is outside the supported demo languages.", "human_only", layer="input")
    if INJECTION_RE.search(message):
        return block(
            "Unsafe instruction blocked",
            "Ticket instructions cannot change merchant scope. No draft is generated.",
            "human_only",
            layer="input",
        )
    if ticket.get("sensitiveInput") or sanitize_input(message)["flagged"]:
        return block(
            "Sensitive input needs manual handling",
            "No generation or message-body export is available for this input.",
            "human_only",
            layer="input",
        )
    if intent != "tracing":
        gate = {
            "dispute": "Dispute specialist required",
            "compliance": "Compliance specialist required",
            "legal": "Legal threat requires a specialist",
        }.get(intent, "Financial action requires a specialist")
        queue = {"dispute": "Tier-2 disputes", "compliance": "Tier-2 compliance"}.get(intent, "Tier-2 payments")
        return block(
            gate,
            "Account context is available. No deadline, regulatory diagnosis, hold release, refund or execution advice is generated.",
            "human_only",
            queue,
            layer="input",
        )
    if account.get("kyc") != "Verified":
        return block(
            "Account review flag needs a specialist",
            "The account carries a review flag. No diagnosis or release advice is generated.",
            "human_only",
            "Tier-2 compliance",
        )
    if extracted["invalidAmount"] or UNSUPPORTED_MONEY_RE.search(message):
        return block(
            "Unsupported monetary input",
            "Confirm the exact positive amount, currency and supported precision with the merchant.",
            layer="input",
        )

    scoped = [tx for tx in data["transactions"] if tx.get("merchant") == ticket.get("merchant")]
    refs = [confirmed_reference.strip().upper()] if confirmed_reference else extracted["references"]
    if refs:
        matches = [tx for tx in scoped if tx.get("id") in refs or tx.get("reference") in refs]
    else:
        matches = [
            tx
            for tx in scoped
            if any(a["minor"] == tx.get("amountMinor") and a["currency"] == tx.get("currency") for a in extracted["amounts"])
        ]
    if any(_bad_source(tx) for tx in matches):
        return block("Invalid source schema", "A required source field is missing or malformed. Use manual investigation.")
    base["candidates"] = [dict(tx) for tx in matches]
    base["sources"] = [s for tx in matches for s in source_records(tx)]
    if not matches:
        return block(
            "Reference unavailable in this account" if refs else "Payment reference needed",
            "Ask the merchant for a unique reference and verify the currency. Do not infer ownership of an unavailable reference.",
        )
    if len(matches) != 1 or not refs:
        return block(
            "A unique payment reference is needed",
            "An amount alone cannot confirm a transaction. Record the reference supplied by the merchant, or hand over with the authorized candidates.",
        )
    tx = matches[0]
    if any(ref not in (tx["id"], tx["reference"]) for ref in refs):
        return block(
            "Conflicting transaction references",
            "The request contains references that do not identify the same authorized payment. Clarify the merchant’s reference before drafting.",
        )
    if extracted["amounts"] and not all(
        a["currency"] == tx["currency"] and a["minor"] in (tx["amountMinor"], tx.get("netMinor")) for a in extracted["amounts"]
    ):
        return block(
            "Amount or currency mismatch",
            "The request does not match this transaction. No silent FX conversion or amount-only match is allowed.",
        )
    received, fetched = _ms(ticket.get("receivedAt")), _ms(tx["fetchedAt"])
    age = received - fetched if received is not None and fetched is not None else None
    if age is None or age < 0 or age > 300000:
        return block(
            "Source snapshot needs refreshing",
            "The fixture snapshot is missing, in the future or older than five minutes at request time. Return to a person; reopening does not make data fresh.",
        )
    if tx.get("clearingStatus") and tx["clearingStatus"] != tx["status"]:
        return block(
            "Conflicting source records",
            "The ledger and clearing record disagree. Both are available for investigation; no definitive status draft is generated.",
        )
    if "feeMinor" in tx and (
        not _safe_int(tx["feeMinor"])
        or tx["feeMinor"] < 0
        or not _safe_int(tx.get("netMinor"))
        or tx["netMinor"] <= 0
        or tx["amountMinor"] - tx["feeMinor"] != tx["netMinor"]
    ):
        return block("Fee reconciliation failed", "The documented gross, fee and net do not reconcile.")
    method = tx.get("matchMethod")
    if "matchMethod" in tx and method not in ("reference", "model"):
        return block("Unknown matching method", "Use manual investigation for unrecognized matching provenance.")
    score = tx.get("matchScore")
    if method == "model" and (not _is_number(score) or not 0.95 <= score <= 1):
        return block(
            "Model confidence requires manual review",
            "A model-derived match requires a finite score from 0.95 to 1, in addition to all identity and evidence checks.",
        )

    base["transaction"] = tx
    base["state"] = "draft_ready"
    base["gate"] = "Unique reference · merchant and payment verified"
    base["checks"] = [
        "Merchant scope",
        "Unique reference",
        "Amount and currency",
        "Snapshot freshness",
        "Consistent status",
        "Evidence citations",
    ]
    base["draft"] = make_draft(ticket, tx)
    if not evaluate_draft(base, base["draft"])["passed"]:
        return block("Reply checks failed", "Generated wording did not pass deterministic checks.", layer="output")
    base["layer"] = None
    return base


# ── output guardrails ───────────────────────────────────────────────────────
PROMISE_RE = re.compile(
    r"\b(guarantee|guaranteed|garanti|garantiert)\b|(?:arrive|credited|paid|refund|settle).{0,25}(?:tomorrow|today|within|by \d)|(?:demain|morgen).{0,25}(?:credit|gutgeschr|erstatt)|(?:released|refunded|transferred).{0,15}(?:funds|money)",
    re.IGNORECASE | re.ASCII,
)
COMMITMENT_RE = re.compile(
    r"\b(we|i)('ll| will| shall| are going to| can)\s+(credit|refund|reimburse|reverse|cancel|waive|compensate|pay|resend|release|transfer)|your (refund|reimbursement|credit)\b.{0,20}\b(is|has been|was|will be)\b.{0,10}\b(on its way|approved|processed|issued|initiated|sent)|(fee|charge)s?\b.{0,15}\b(waived|refunded|removed|cancel)|\bwaive|\b(compensation|reimbursement)\b|\bentitled to\b|(will|should)\s+(arrive|be credited|reach|land|be paid|be received)|next (week|monday|tuesday|wednesday|thursday|friday)|\bunder (psd2|the law|article)|rembourserons|recrediterons|nous (allons|pouvons|devons) (vous )?(rembourser|recrediter|annuler)|vous serez (rembourse|recredite)|indemnis|geste commercial|vous avez droit|arrivera|sera credite|devrait (arriver|etre credite)|semaine prochaine|sous \d+ jours|erstatten wir|wir (werden|erstatten|buchen)|wird (ihnen )?(erstattet|zuruckgebucht)|entschadig|anspruch auf|erlassen|nachste woche|innerhalb von \d+|wird.{0,30}(ankommen|gutgeschrieben werden|eingehen)",
    re.ASCII,
)
UPGRADE_RE = re.compile(r"\b(definitely paid|has been credited|was credited|est credite|wurde gutgeschrieben)\b", re.ASCII)

# Stable codes for dashboards and API clients; the issue text matches the JS.
ISSUES = {
    "no_transaction": "No verified, answerable transaction.",
    "empty": "Reply is empty.",
    "sensitive": "Sensitive input must be removed before reply preparation.",
    "promise": "Unsupported promise or financial action.",
    "commitment": "Unsupported promise, money action or legal claim.",
    "amount": "Amount or currency is not supported by the matched source.",
    "reference": "Reference is not supported by the matched transaction.",
    "citation": "Missing or invalid transaction citations.",
    "status_upgrade": "The reply upgrades the recorded payment status.",
    "manual_review": "Edited wording needs a manual factual review; the rules cannot certify free text.",
}


def evaluate_draft(analysis: dict[str, Any], text: str) -> dict[str, Any]:
    tx = analysis.get("transaction")
    if not tx or analysis.get("state") != "draft_ready":
        return {"passed": False, "critical": True, "issues": [ISSUES["no_transaction"]], "codes": ["no_transaction"]}
    codes: list[str] = []
    n = normalize(text)
    if not text.strip():
        codes.append("empty")
    if sanitize_input(text)["flagged"]:
        codes.append("sensitive")
    if PROMISE_RE.search(text):
        codes.append("promise")
    if COMMITMENT_RE.search(n):
        codes.append("commitment")
    financial = entities(text)
    if any(
        a["currency"] != tx["currency"] or a["minor"] not in (tx["amountMinor"], tx.get("feeMinor"), tx.get("netMinor"))
        for a in financial["amounts"]
    ):
        codes.append("amount")
    if any(r not in (tx["reference"], tx["id"]) for r in financial["references"]):
        codes.append("reference")
    ids = re.findall(r"\b(?:LED|CLE)-[A-Z0-9-]+\b", text)
    if any(i not in (tx["ledger"], tx["clearing"]) for i in ids) or not all(i in ids for i in (tx["ledger"], tx["clearing"])):
        codes.append("citation")
    if tx["status"] != "credited" and UPGRADE_RE.search(n):
        codes.append("status_upgrade")
    language = "FR" if text.startswith("Votre") else "DE" if text.startswith("Ihre") else "EN"
    canonical = make_draft({"language": language}, tx)
    exact = " ".join(text.split()) == " ".join(canonical.split())
    critical = bool(codes)
    if not critical and not exact:
        codes.append("manual_review")
    return {"passed": not codes, "critical": critical, "issues": [ISSUES[c] for c in codes], "codes": codes}


def handover(ticket: dict[str, Any], analysis: dict[str, Any], reason: str, note: str) -> dict[str, Any]:
    if not reason.strip() or (reason == "Other — see agent note" and not note.strip()):
        raise ValueError("A reason and, for Other, an agent note are required.")
    return {
        "ticket": ticket.get("id"),
        "merchant": ticket.get("merchant"),
        "queue": analysis["queue"],
        "reason": reason,
        "note": sanitize_input(note.strip())["text"],
        "gate": analysis["gate"],
        "sources": [{"id": s["id"], "fetchedAt": s["fetchedAt"]} for s in analysis["sources"]],
        "policy": "FLOW-POL-1",
        "demo": True,
    }
