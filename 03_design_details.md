# 03 — Design details · FlowAssist · v2

**Team:** Lenny Santus, Anthony Rascle, Antoine Rabeau, Benjamin Caujolle, Colin Sibieude · **P2** · **3 November 2026**
**Status:** v2 design complete; decisions D01–D05 in `03_user_research.md` derive from desk analysis. No participant validation is claimed.

## 1. Problem, user, do-nothing
Karim, a Tier-1 payment operations specialist, loses 7.2 of an 18-minute ticket to investigation across disconnected tools. FlowAssist reconstructs a payment timeline and drafts a cited reply inside Zendesk; Karim checks and sends it. The P2 case provides 800 merchants, 12,000 tickets/month and 40% investigation time; the 18-minute baseline, staffing and detailed economics are inherited S1/S2 scenario assumptions, not newly observed company data. Without it: manual search and macros, 4% annual efficiency improvement (€57,600/year), against a €125,000/year alternative project.

## 2. Process — as-is → to-be
**Fallback first:** at every step, “Escalate with context” preserves the ticket, safe evidence, block reason and agent notes for Tier-2. A failed identity check exposes no transaction context. Agents can dismiss the copilot and continue manually. No customer message or financial write is available to the copilot.

Minutes are **active human time**, including review. All step splits, error rates and after-times below are **guesses**, retaining S1's 18-minute total; validate with paired timing. Error costs are S2 judgement (€15 tracing; €90 dispute; €150 compliance), not measured incident rates. Rates are step-specific, not additive.

| # | Step; today: Tier-1 specialist | Before min | Error rate (guess) | Cost/error | Decision; failed S3 test | Trust | After min (guess) | Step metric |
|---|---|---:|---:|---|---|---|---:|---|
| 1 | Read ticket, establish merchant and intent | 1.5 | 3% wrong/missing reference | €15; disclosure tail unpriced | Augment; T1 unclear input, T6 expensive identity error | L1 suggests; identity verified by backend | 1.0 | Wrong-tenant attempts blocked: 100% |
| 2 | Search ledger and clearing logs **(pain)** | 5.7 | 2.5% wrong match | €15; disclosure tail unpriced | Augment matching; automate exact read-only lookup only; T4 multi-source chain, T6, T7 live status | L3 internal candidate retrieval, human confirms match | 1.5 | Unique correct match; lookup latency p95 ≤2s target |
| 3 | Write reply and attach sources **(pain)** | 4.8 | 2.5% unsupported claim | €15; €90 if deadline invented | Augment; T5 explanation, T6 cost | L2 draft, approval required | 0.8 | Cited factual claims; two-grader usability |
| 4 | Check status, policy and constraints | 2.5 | 2% missed restriction | €90–150; tail unpriced | Augment; T5, T6, T7 changing rules | Rules block automatically; specialist L2 validation | 1.3 | Unsafe drafts exposed: 0 |
| 5 | Review, edit, approve and send | 2.0 | 1% residual wrong answer | €15–150; tail unpriced | Keep human; T3 delayed reopen feedback, T5, T6 | Person only | 2.0 | QA ≥92%; unauthorized sends: 0 |
| 6 | Categorize, log and hand over if needed | 1.5 | 3% wrong routing | €15 rework | Automate event logging, augment routing; T1 ambiguous intent, T6 urgent cases | L4 append-only metadata; L1 route suggestion | 1.0 | Complete audit events; handover delivery |
| | **Total** | **18.0** | | | | | **7.6** | **57.8% hypothesized saving** |

T1–T8 refer to S3 slide 14: clear I/O, examples, feedback, short reasoning, limited explanation, cheap errors, stable world, screen work. T2 is unproven without a labelled corpus; T8 passes. The 7.6-minute target is for eligible tracing cases, not all tickets. **The governance line:** verified tenant and unique transaction before drafting; human approval before any customer communication. The former L4 model-based matching proposal is narrowed: an LLM score cannot authorize data access.

## 3. Features — RICE and MoSCoW
RICE = reach × impact × confidence / person-weeks. Reach uses `02_sizing.xlsx` Inputs D6, D14:D20: 6,000 tracing/month, of which 4,500 eligible; 3,600 disputes; 2,400 compliance. Impact, confidence, effort and feature coverage are planning guesses. Sorted scores rank value, not permission to automate.

| Candidate feature | Reach/month | Impact | Confidence | Effort weeks | RICE | MoSCoW |
|---|---:|---:|---:|---:|---:|---|
| Tenant/policy gate + context-only fallback + escalation | 12,000 | 3 | 80% | 2 | 14,400 | MUST |
| Cited tracing timeline and editable draft | 4,500 | 3 | 50% | 2 | 3,375 | MUST |
| Categorization and CRM tag suggestions | 12,000 | 0.25 | 80% | 1 | 2,400 | WON'T |
| Paired timing and grader capture, including fallbacks | 4,500 | 2 | 80% | 3 | 2,400 | MUST |
| Autonomous merchant replies | 6,000 | 2 | 50% | 4 | 1,500 | WON'T |
| Dispute deadline drafting | 3,600 | 2 | 50% | 3 | 1,200 | WON'T |
| KYC/AML hold explanations or release advice | 2,400 | 2 | 50% | 3 | 800 | WON'T |
| Refund / settlement execution | 6,000 | 1 | 50% | 5 | 600 | WON'T |

**MUST (3):** safe gate/handover; cited tracing draft; paired measurement. **SHOULD:** citation preview usability polish after tests. **COULD:** agent feedback shortcut. These refinements do not expand functional scope. **WON'T (5):** the five rows above; tagging remains manual. Additional boundaries: no customer chatbot, no model training on tickets, no unsupported languages or FX conversion advice. The draft and timing features test the **41.2% time-saving flip assumption** and are MUST despite lower RICE. The hardest cut is dispute drafting: attractive value, but deadline errors are costly and it does not test the dominant assumption.

## 4. Data
Coursework: synthetic tickets and self-contained ledger snapshots only; 20 proposed cases, AI-generated labels awaiting human approval. No PayFlow exports are present. Future sources: authenticated merchant context, read-only ledger, clearing events and versioned policy; rights, freshness, tenant filtering and retention in `governance.md` §Session 3. Initial scope: FR/EN/DE, EUR SEPA and USD SWIFT, EU merchants; coverage is qualitative, not representative.

## 5. Model — smallest rung per component
| Part | Rung | Why the rung below fails / why stop here |
|---|---|---|
| Auth, tenant filter, exact lookup, freshness, policy blocks | 1 — rules | No lower rung; exact invariants must not depend on model confidence |
| Intent / amount / reference extraction | 3 — pretrained model, structured output | Rung 2 needs unavailable human-labelled training data; test reference/keyword rules first and retain them if sufficient |
| Timeline and reply | 4 — hybrid: deterministic join + retrieved facts + pretrained drafting | Rung 3 alone has no current ledger facts or enforceable isolation; compare with rule templates before choosing the LLM |
| Grounding | 4 — exact claim checks + model critique | Rung 3 judge alone cannot enforce exact amounts, tenant identity or citations; rules remain mandatory and critique cannot override a block |
| Timing, audit and handover | 1 — rules | Event capture and routing do not need ML |

Choices are hypotheses for S4 ablation, not evaluated superiority. No fine-tuning or dual-model safety guarantee is assumed.

## 6. Integration surface
Zendesk sidebar beside original ticket: verified merchant, transaction candidates, source timestamps, cited editable draft, review checkbox, “Use draft in editor”, “Escalate with context” and “Continue manually”. Customer send remains in the human inbox. Inputs/outputs and block states: `spec.md`. Retrieval p95 ≤2s and total draft p95 ≤10s are targets; on timeout fail closed. Logs: assigned agent and authorized Ops QA; security metadata for CISO; minimized audit export under DPO control. Local clickable surface: `prototype/index.html` v0.3 (synthetic, no API), with search/filters, visible review progress, isolated in-tab ticket buffers, explicit replacement confirmation and keyboard shortcuts. Source inspection and approval reset on ticket selection; text is restored only for its owning ticket.

## 7. Success criterion
> By 8 November 2026, on a frozen 200-case synthetic tracing benchmark with eligibility labelled before execution and paired human timing, FlowAssist saves at least 41.2% of total active handling time on eligible cases versus manual handling, including review and fallback time, with QA ≥92%, grounding-check precision ≥98%, and zero wrong-transaction disclosures, cross-tenant exposures, unauthorized sends or monetary actions.

S3 delivers **20 seed cases**, not the 200-case benchmark or measured success. Timing formula and rubric: `evals/README_eval_set.md`. The threshold is inherited from S2; S3 does not replace it with Paylio's 45% draft acceptance. The original S2 value includes disputes and compliance contributions: a tracing-only pass authorizes further validation, **not** the full €141k business case or production rollout. Scope economics and token costs need reassessment before investment.

## 8. Risks and rollback
Wrong match, fabricated settlement certainty, stale clearing feeds, prompt injection, tenant leakage and review fatigue. One unsafe exposure or attempted send/fund write → disable drafting immediately, preserve minimized evidence and route manually; Ops Lead owns the stop, Engineering enforces it, DPO/CCO assesses any data incident. A failed timing/quality gate means conditional NO-GO and redesign, not a lowered threshold.

## 9. What the users changed — v2 design register
No user-driven changes are established. The v2 implements D01 all-source inspection, D02 direct missing-reference wording, D03 timestamped evidence/handover, D04 a compliance destination, and D05 disabling insertion after manual fallback. Each decision has an acceptance scenario in [the needs and decision record](03_user_research.md). Scope and the 41.2% economic threshold stay fixed. [Original brief v1](research/brief_v1.md) records the prior design.

## 10. What users could not decide
Users can change placement, wording and handover ergonomics. CFO/Product owns the 41.2% economic hurdle; paired timing and independent graders judge performance; Engineering chooses model after ablation; DPO/Legal confirms lawful processing, contracts and retention; CCO/Ops approves allowed scope. None is established by favourable interview opinions.
