"""Compare two independent labeller exports and fill the v1 review files.

Usage: python3 scripts/merge_labels_v1.py labels_v1_Alice.csv labels_v1_Bob.csv

- Writes both reviewers' names, dates and agree/disagree decisions into evals/label_review_v1.csv.
- Copies labels into evals/eval_set_v1.csv only where both reviewers agree on the state,
  handover, case type and eligibility (reviewer 1's wording is kept for the free text).
- Prints the disagreements; a third person adjudicates them, writes the reason in the
  `adjudication` column and edits the case in eval_set_v1.csv by hand.
Never runs the engine.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYS = ["state", "hand_over_to_a_person", "case_type", "eligible_for_timing"]


def read(path):
    with Path(path).open(newline="", encoding="utf-8") as stream:
        return {r["id"]: r for r in csv.DictReader(stream)}


def decision(r):
    return {**r, "state": r["expected_output_or_action"].split(";")[0].strip()}


if len(sys.argv) != 3:
    sys.exit(__doc__)
first, second = (read(p) for p in sys.argv[1:])
ids = [f"V{i:03}" for i in range(1, 201)]
missing = [i for i in ids if not all(d.get(i, {}).get("case_type") for d in (first, second))]
if missing:
    sys.exit(f"Both exports must be complete. Missing or unlabelled: {missing[:10]}{' …' if len(missing) > 10 else ''}")
names = {next(iter(d.values()))["labeller"] for d in (first, second)}
if len(names) != 2:
    sys.exit("The two exports come from the same labeller; independent reviews are required.")

eval_path, review_path = ROOT / "evals/eval_set_v1.csv", ROOT / "evals/label_review_v1.csv"
with eval_path.open(newline="", encoding="utf-8") as stream:
    reader = csv.DictReader(stream)
    columns, rows = reader.fieldnames, list(reader)
with review_path.open(newline="", encoding="utf-8") as stream:
    reader = csv.DictReader(stream)
    review_columns, reviews = reader.fieldnames, {r["case_id"]: r for r in reader}

disagreements = []
for row in rows:
    a, b = decision(first[row["id"]]), decision(second[row["id"]])
    diff = [k for k in KEYS if a[k] != b[k]]
    review = reviews[row["id"]]
    review.update(reviewer_1=a["labeller"], review_1_date=a["labelled_at"], reviewer_2=b["labeller"],
                  review_2_date=b["labelled_at"], review_1_decision="agree" if not diff else f"differs: {', '.join(diff)}",
                  review_2_decision="agree" if not diff else f"differs: {', '.join(diff)}")
    if diff:
        disagreements.append((row["id"], {k: (a[k], b[k]) for k in diff}))
        continue
    for k in ["expected_output_or_action", "hand_over_to_a_person", "case_type", "eligible_for_timing", "evidence_or_source", "notes"]:
        row[k] = a[k]

with eval_path.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, columns)
    writer.writeheader()
    writer.writerows(rows)
with review_path.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, review_columns)
    writer.writeheader()
    writer.writerows(reviews[i] for i in ids)

print(f"Agreed and copied: {200 - len(disagreements)}/200. To adjudicate: {len(disagreements)}.")
for case_id, diff in disagreements:
    print(case_id, "; ".join(f"{k}: {x!r} vs {y!r}" for k, (x, y) in diff.items()))
