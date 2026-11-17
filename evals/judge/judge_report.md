# Judge report — gpt-6-luna

Guideline: `evals/judge/rubric.md` (judge prompt = guideline, copied). Inputs: 15 drafts of the development set + 41 known-bad variants.

| Measure | Value |
|---|---|
| Human–human agreement (grader 1 vs grader 2, sendable yes/no) | n/a |
| Human–judge agreement, grader 1 | 11/15 = 73% |
| Human–judge agreement, grader 2 | n/a |
| Known-bad variants escalated by the judge | 41/41 |
| Known-bad variants the judge called sendable (over-acceptance) | 0: none |
| Tokens (input / output / cache read) | 41690 / 11468 / 0 |

Limits: the drafts are templates on a development set already examined by the team, and grader 1 also reviewed the labels. Agreement on 15 cases is a small sample. Read the disagreements in `evals/judge/judge_results.json` before trusting the number; fix the guideline once, re-measure, then sample 5 % weekly.
