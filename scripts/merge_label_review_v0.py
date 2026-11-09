"""Fill evals/label_review.csv from one or two label reviews (evals/label_review.html).

Usage: python3 scripts/merge_label_review_v0.py label_review_v0_<A>.csv [label_review_v0_<B>.csv]

- Each export must cover all 50 cases (approved or corrected), from different people.
- Records reviewer names, dates and decisions; never edits eval_set_v0.csv itself.
- Lists every correction: the team applies agreed corrections to eval_set_v0.csv by hand
  and notes them in `adjudication`. The 50 cases stay development data either way.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    with Path(path).open(newline="", encoding="utf-8") as stream:
        return {r["case_id"]: r for r in csv.DictReader(stream)}


if len(sys.argv) not in (2, 3):
    sys.exit(__doc__)
exports = [read(p) for p in sys.argv[1:]]
ids = [f"F{i:02}" for i in range(1, 51)]
for e in exports:
    missing = [i for i in ids if e.get(i, {}).get("decision") not in ("approved", "corrected")]
    if missing:
        sys.exit(f"Incomplete review from {next(iter(e.values()))['reviewer']}: {missing[:10]}")
names = [next(iter(e.values()))["reviewer"] for e in exports]
if len(set(names)) != len(names):
    sys.exit("Both exports come from the same reviewer.")

path = ROOT / "evals/label_review.csv"
with path.open(newline="", encoding="utf-8") as stream:
    reader = csv.DictReader(stream)
    columns, rows = reader.fieldnames, list(reader)
corrections = []
for row in rows:
    for n, e in enumerate(exports, start=1):
        r = e[row["case_id"]]
        decision = r["decision"] if r["decision"] == "approved" else f"corrected: {r['corrected_state'] or 'same state'}, {r['corrected_case_type'] or 'same type'}"
        row.update({f"reviewer_{n}": r["reviewer"], f"review_{n}_date": r["date"], f"review_{n}_decision": decision})
        if r["decision"] == "corrected":
            corrections.append((row["case_id"], r["reviewer"], decision, r["comment"]))
with path.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

approved_by_all = sum(all(e[i]["decision"] == "approved" for e in exports) for i in ids)
print(f"Reviewed by {' and '.join(names)}. Approved by every reviewer: {approved_by_all}/50. Corrections: {len(corrections)}.")
for case_id, who, decision, comment in corrections:
    print(f"{case_id} ({who}): {decision} | {comment}")
