# 03 — Product brief · FlowAssist · v2

**P2 · PayFlow AI Product Team · 3 November 2026**
**Status:** v2 design complete; desk-based revision plus three conversations and a prototype try-out on 9 November (D06–D08); desirability not validated. [Original v1](research/brief_v1.md). [Process, scoring and model tables](03_design_details.md) form the supporting annex.

## 1. Problem, user, do-nothing
Karim, Tier-1 payment Ops specialist, investigates disconnected records before replying. P2 provides 800 merchants, 12,000 tickets/month and 40% investigation time; S1 assumes 18-minute handling time, including 7.2 minutes investigation. Do nothing: manual tools/macros and 4% annual efficiency gain (€57,600), versus a €125,000 alternative project. No actual internal logs or time study are available here.

## 2. The process — as-is and to-be
Six human steps: read **1.5→1.0 min**; search **5.7→1.5**; draft **4.8→0.8**; check **2.5→1.3**; review/send **2.0→2.0**; log **1.5→1.0**. Before **18.0**, after **7.6 min**, a **57.8% hypothesis on eligible tracing**, not a result. The two pain steps are search and drafting. Step-level error rates, cost, source types, failed automation tests and metrics: [annex §2](03_design_details.md#2-process--as-is--to-be).

L1 entity suggestions → L3 tenant-scoped candidate retrieval → human match confirmation → L2 cited draft and checks → **person-only send**; bounded audit metadata L4. At any step, manual handling or escalation preserves safe evidence and reason. Failed identity exposes no transaction data. The governance line is verified tenant/transaction before drafting, then human approval before communication.

## 3. Features — RICE and MoSCoW
**MUST (3):** tenant/policy gate with handover; cited tracing timeline/draft; paired timing and grading. **SHOULD:** citation-preview polish. **COULD:** feedback shortcut. **WON'T (5):** automatic CRM tags, autonomous replies, dispute deadlines, KYC/AML explanations, refunds/settlement execution. [Eight scored candidates, sorted RICE](03_design_details.md#3-features--rice-and-moscow). Reach: 6,000 tracing/month ×75% eligible =4,500, from S2.

Drafting plus timing tests the flip assumption, so both are MUST despite lower RICE. The hardest cut is dispute drafting: attractive value, costly deadline errors and no direct test of the dominant assumption.

## 4. Data
20 self-contained synthetic cases; AI-proposed labels await human approval. Future sources: authenticated merchant session, read-only ledger/clearing events, versioned policy. FR/EN/DE, EUR SEPA and USD SWIFT initially; rights, retention, isolation and gaps in [governance S3](governance.md#session-3--data-and-trust-levels--2-november-2026).

## 5. Model — one rung per part
Rules for permissions, money, freshness and audit; pretrained structured extraction because no labelled training corpus exists; hybrid retrieval/drafting because a standalone pretrained model has no current ledger facts; exact checks plus model critique because an LLM judge cannot enforce identity. [Component choices and lower-rung alternatives](03_design_details.md#5-model--smallest-rung-per-component); test rule templates first in S4.

## 6. Where it lives
Zendesk sidebar: verified merchant, source timestamps, editable cited draft, all-source inspection, explicit review and timestamped specialist handover. Manual mode disables draft insertion; compliance routes to its specialist. Targets: retrieval p95 ≤2s, complete draft ≤10s; timeout suppresses drafting. Logs restricted to assigned agent and authorized Ops/security reviewers. [Local clickable prototype](prototype/index.html), no live connections.

## 7. Success criterion
> By 8 November 2026, on a frozen 200-case synthetic tracing benchmark with eligibility labelled before execution and paired human timing, FlowAssist saves at least 41.2% of total active handling time on eligible cases versus manual handling, including review and fallback time, with QA ≥92%, grounding-check precision ≥98%, and zero wrong-transaction disclosures, cross-tenant exposures, unauthorized sends or monetary actions.

S3 supplied 20 seeds; the current S4 development set contains 50 cases and does not establish measured business success. [Denominator and grading](evals/README_eval_set.md). A tracing-only pass does not validate S2's dispute/compliance value or authorize production.

## 8. Risks and rollback trigger
Wrong match, stale facts, fabricated certainty, injection and review fatigue. Any critical exposure or attempted send/fund write immediately disables drafting; Ops owns the stop, Engineering enforces it, DPO/CCO assesses the incident. Failed performance means redesign, not a lowered threshold.

## 9. What the users changed
Three conversations on 9 November (two people drawing on past accounting and support jobs, one classmate in role; [record](03_user_research.md)) led to three changes:
- **D06 · Next step and follow-up time** in every context-only or handover reply. Evidence: P2 « je lui dis précisément quelle est la prochaine étape et quand il aura de nos nouvelles », P3 « un délai de suivi ».
- **D07 · Documented typical processing time**, labelled "typical, not guaranteed", never a date for this payment. Evidence: P1 « une estimation du délai si on en a une », P2 « le délai habituel ». Pending Ops/Legal approval.
- **D08 · Plain-language status wording.** Evidence: P2 « pas avec du jargon bancaire ».

They confirmed sent ≠ credited (P2), no promised date (P1), asking for a reference before handing over (P1) and escalating when unsure (P3). D01–D05 remain team design decisions. The prototype try-out recorded only a positive impression, so no usability change is claimed.

## 10. What users could not decide
Users could not settle whether a typical delay reassures the merchant or reads as a promise (P1 wants an estimate but no promised date): Ops and Legal decide D07. CFO/Product owns the 41.2% hurdle; timing and independent graders establish performance; Engineering selects the model after evaluation; DPO/Legal confirms lawful use and retention; CCO/Ops approves scope. Users inform workflow and wording.
