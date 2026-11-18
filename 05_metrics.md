# 05 — Metrics · FlowAssist

## 1. Measurement stack

| Level | Metric and source |
|---|---|
| Rules | Extraction regression and browser/server decision parity. |
| AI system | Correct routing and sendable-as-is rate on frozen eligible cases. |
| Guardrails | Count human-only drafts, foreign evidence, wrong matches and prohibited financial commitments. |
| Product | Draft acceptance, edits, handovers, and handling time p50/p95 by language and plan. See the [tracking plan](docs/TRACKING_PLAN.md). |
| Business | Active time, audited reply quality and seven-day reopens in both pilot arms. |

## 2. Stop rule

One critical escape blocks release or stops assisted drafting. A critical escape includes foreign evidence, a wrong match, a human-only draft or a prohibited commitment released. Head of Payment Operations owns the decision and the on-call engineer can activate the switch.

## 3. Hierarchy and segment limits

- **Primary:** reduction in mean active minutes per assigned eligible ticket versus manual work, including fallbacks and handovers.
- **Guardrails:** zero critical escapes, QA ≥92/100 and grounding-check precision ≥98% (valid claims among claims accepted by the check).
- **Counter-metrics:** seven-day reopens ≤ control +2 percentage points and manual handovers ≤ control +5 points on eligible work. These are proposed pilot limits. Report overall and by language, plan and rail. Hold expansion where sparse samples leave harm unresolved.

## 4. Three business effects

| Metric | Baseline → hypothesis at pilot readout | Link to evidence |
|---|---|---|
| Active time | Concurrent manual mean → ≥41.2% reduction. Workbook base assumes 48%. | Time-equivalent benefit and investment hurdle. |
| Audited QA | Concurrent manual audit → ≥92/100 with no deterioration versus manual. | Sizing error costs depend on reply quality. |
| Seven-day reopens | Concurrent manual rate → no more than +2 points. | Rework can erode time savings and modeled SLA benefits. |

See [sizing](02_sizing.xlsx), [investment memo](02_investment_memo.md) and [S4 report](evals/report_v0.md). The S4 regression does not measure these business effects.

## 5. Evaluation

The [sample manifest](evals/v1/assignment5_sample.csv) selects 100 synthetic v1 cases and a nested set of 30 by language, plan and rail using proportional quotas. Record the policy version and commit when reviewed labels are frozen. Merge reviewed labels with provenance. Keep the 50 exposed v0 cases for regression.

Two blind humans and the judge independently score the same 30 cases with identical evidence, including refusal and routing outcomes. Report exact human–human and judge–adjudicated-human agreement with denominators, disagreement categories and changes to the rubric. Below 80%, revise the rubric and remeasure.

Current evidence: 200 aligned inputs and 0/200 labels merged in the benchmark. Lenny’s 44-row export is available with provenance restrictions. Historical agreement was 11/15 against one human on development drafts. Four disagreements reveal a reply-language defect. The second independent grader and comparable 30-case results remain pending. [Eval guide](evals/README.md) · [Judge prompt](evals/judge_prompt.txt) · [Judge report](evals/judge/judge_report.md)
