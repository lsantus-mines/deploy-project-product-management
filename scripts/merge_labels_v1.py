"""Merge the labellers' exports for eval-set v1 and fill the review files.

Usage: python3 scripts/merge_labels_v1.py labels_v1_*.csv

Each member labels a block of 40 cases plus 4 shared cases from the previous block
(see evals/README_eval_set.md), so most cases have one label and 20 have two.
- Refuses to write anything until all 200 cases are labelled by at least one person.
- Copies single labels, and double labels that agree on state, handover, case type and
  eligibility, into evals/eval_set_v1.csv (the first labeller's wording is kept).
- Fills evals/label_review_v1.csv with who labelled what, and when.
- Prints the agreement rate on the shared cases and lists disagreements; a third person
  adjudicates each one, writes the reason in `adjudication` and edits the case by hand.
Never runs the engine.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEAM = ["Lenny", "Anthony", "Antoine", "Benjamin", "Colin"]  # block owners, in case order
KEYS = ["state", "hand_over_to_a_person", "case_type", "eligible_for_timing"]
COPIED = ["expected_output_or_action", "hand_over_to_a_person", "case_type", "eligible_for_timing", "evidence_or_source", "notes"]


def read(path):
    with Path(path).open(newline="", encoding="utf-8") as stream:
        return [r for r in csv.DictReader(stream) if r.get("case_type", "").strip()]


if len(sys.argv) < 2:
    sys.exit(__doc__)
labels, seen = {}, set()
for path in sys.argv[1:]:
    rows = read(path)
    for name in {r["labeller"] for r in rows}:
        if name in seen:
            sys.exit(f"{name} appears in more than one export; merge each person's work into one export first.")
        seen.add(name)
    for r in rows:
        labels.setdefault(r["id"], []).append({**r, "state": r["expected_output_or_action"].split(";")[0].strip()})

ids = [f"V{i:03}" for i in range(1, 201)]
missing = [i for i in ids if i not in labels]
if missing:
    sys.exit(f"Not complete yet: {200 - len(missing)}/200 labelled. Missing: {', '.join(missing[:15])}{' …' if len(missing) > 15 else ''}")

eval_path, review_path = ROOT / "evals/eval_set_v1.csv", ROOT / "evals/label_review_v1.csv"
with eval_path.open(newline="", encoding="utf-8") as stream:
    reader = csv.DictReader(stream)
    columns, rows = reader.fieldnames, list(reader)
with review_path.open(newline="", encoding="utf-8") as stream:
    reader = csv.DictReader(stream)
    review_columns, reviews = reader.fieldnames, {r["case_id"]: r for r in reader}

shared, disagreements = 0, []
for row in rows:
    owner = TEAM[(int(row["id"][1:]) - 1) // 40]
    found = sorted(labels[row["id"]], key=lambda r: r["labeller"] != owner)  # block owner is reviewer 1
    a = found[0]
    review = reviews[row["id"]]
    review.update(reviewer_1=a["labeller"], review_1_date=a["labelled_at"], review_1_decision="labelled")
    diff = []
    if len(found) > 1:
        shared += 1
        b = found[1]
        diff = [k for k in KEYS if a[k] != b[k]]
        verdict = "agree" if not diff else f"differs: {', '.join(diff)}"
        review.update(reviewer_2=b["labeller"], review_2_date=b["labelled_at"], review_1_decision=verdict, review_2_decision=verdict)
    if diff:
        disagreements.append((row["id"], {k: (a[k], b[k]) for k in diff}))
        continue
    for k in COPIED:
        row[k] = a[k]

with eval_path.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, columns)
    writer.writeheader()
    writer.writerows(rows)
with review_path.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, review_columns)
    writer.writeheader()
    writer.writerows(reviews[i] for i in ids)

print(f"Labelled: 200/200 by {len(seen)} people. Shared cases: {shared}; agreement {shared - len(disagreements)}/{shared}.")
print(f"Copied into eval_set_v1.csv: {200 - len(disagreements)}. To adjudicate: {len(disagreements)}.")
for case_id, diff in disagreements:
    print(case_id, "; ".join(f"{k}: {x!r} vs {y!r}" for k, (x, y) in diff.items()))
