# 08 — Launch memo · FlowAssist

**Decision — Hold live rollout. Continue the synthetic demo and prepare a controlled pilot.**

FlowAssist helps specialists trace payments and review cited replies. Human specialists retain approval and sending responsibility.

## Evidence

The [S4 regression](evals/report_v0.md) reached 50/50 expected states and produced 15 drafts, with zero human-only drafts and zero foreign sources. The held-out labels and independent 30-case judge validation are pending. Historical judge agreement was 11/15 and exposed an unresolved language defect. The 41.2% time-saving threshold and live QA remain unproven. A server switch exists and production rollback rehearsal remains pending.

## Rollout and sign-off

1. **Synthetic validation.** Complete [S5 evaluation](05_metrics.md), resolve the language finding and rehearse rollback in an isolated environment. Product and Engineering sign readiness.
2. **Controlled pilot.** Head of Payment Operations approves eligible traffic, DPO approves data handling and trace retention, and Engineering signs monitoring readiness. Follow the [experiment plan](06_07_experiments_operations.md) with daily safety review.
3. **Limited expansion.** Head of Payment Operations signs after Product review and Finance validation when economics, quality and safety gates pass. A single critical escape immediately stops assistance.

No pilot or launch approval is recorded. [Consolidated brief](product_brief.md) · [Specification](spec.md)
