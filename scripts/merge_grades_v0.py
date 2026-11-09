"""Fill evals/grader_reviews.csv from two independent grading exports (evals/grader.html).

Usage: python3 scripts/merge_grades_v0.py grades_v0_<A>.csv grades_v0_<B>.csv

- Both graders must have graded all 15 drafts, and must be two different people.
- final_decision: "sendable" when both say yes, "not sendable" when both say no,
  "pending adjudication" when they differ (an adjudicator then decides and writes it).
- Prints the number to report against the criterion. Cases without a draft keep
  "no draft" as final decision: nothing was shown to the merchant.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    with Path(path).open(newline="", encoding="utf-8") as stream:
        return {r["case_id"]: r for r in csv.DictReader(stream)}


if len(sys.argv) != 3:
    sys.exit(__doc__)
first, second = (read(p) for p in sys.argv[1:])
results = json.loads((ROOT / "evals/results_v0.json").read_text())["results"]
drafts = [r["id"] for r in results if r["draft"] and r["policyPass"]]
for grades in (first, second):
    missing = [i for i in drafts if grades.get(i, {}).get("sendable") not in ("yes", "no")]
    if missing:
        sys.exit(f"Incomplete export from {next(iter(grades.values()))['grader']}: {missing}")
names = {next(iter(g.values()))["grader"] for g in (first, second)}
if len(names) != 2:
    sys.exit("The two exports come from the same grader; two independent people are required.")

path = ROOT / "evals/grader_reviews.csv"
with path.open(newline="", encoding="utf-8") as stream:
    reader = csv.DictReader(stream)
    columns, rows = reader.fieldnames, list(reader)
both_yes = pending = 0
for row in rows:
    if row["case_id"] not in drafts:
        row["final_decision"] = "no draft"
        continue
    a, b = first[row["case_id"]], second[row["case_id"]]
    row.update(grader_1=a["grader"], grader_1_date=a["date"], sendable_1=a["sendable"], rationale_1=a["rationale"],
               grader_2=b["grader"], grader_2_date=b["date"], sendable_2=b["sendable"], rationale_2=b["rationale"])
    if a["sendable"] == b["sendable"]:
        row["final_decision"] = "sendable" if a["sendable"] == "yes" else "not sendable"
        both_yes += a["sendable"] == "yes"
    else:
        row["final_decision"] = "pending adjudication"
        pending += 1
with path.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

agree = len(drafts) - pending
print(f"Drafts graded: {len(drafts)} by {' and '.join(sorted(names))}. Agreement: {agree}/{len(drafts)}.")
print(f"Sendable without editing (both yes): {both_yes}/{len(drafts)} drafts = {both_yes}/50 cases. Pending adjudication: {pending}.")
