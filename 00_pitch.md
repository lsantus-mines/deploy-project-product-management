# 00 — Pitch: FlowAssist (Agent-Assist Copilot for B2B Payments)

> Project proposal P2 (B2B payments fintech) adapted for PayFlow B2B. Committed before Session 3. Customer-support copilot for enterprise merchants.

**The company:**  
PayFlow B2B is a European payment service provider (PSP) and clearing infrastructure fintech serving 800 merchant platforms (B2B marketplaces, enterprise SaaS, corporate distributors). PayFlow processes €4.2B in annual transaction volume across card acquiring, SEPA direct debits, and cross-border SWIFT wires. The customer support team consists of 18 Tier-1 payment operations specialists handling 12,000 inquiries per month.

**The pain, as a cost:**  
Payment support agents spend 40% of their handling time (7.2 minutes out of an 18-minute average handling time) manually investigating across 6 disconnected backend databases: internal PostgreSQL ledgers, banking clearing gateways (SEPA/SWIFT GPI logs), card dispute portals, and KYC/compliance engines. At 144,000 tickets per year and a fully loaded support cost of €10.00/ticket, this manual pre-reading and database investigation costs **€414,720 per year in wasted labor** and drives a slow median first-response time of 4.5 hours. For enterprise merchants reconciling daily liquidity, slow answers trigger SLA penalties (~€35,000/year) and risk merchant churn on key accounts.

**Do-nothing baseline:**  
If no agent is built over the next 12 months, natural learning curves and macro tweaks produce a minor 4% productivity gain (~€57,600/year). However, merchant volume is projected to grow 25% year-on-year (to 15,000 tickets/month). Absorbing this volume while maintaining SLAs would require hiring 4 additional Tier-1 agents at an incremental payroll cost of €220,000/year. Furthermore, manual agent context switching maintains high operational burnout (30% annual agent turnover) and risks costly human errors in dispute filings.

**The agent's job:**  
When a merchant opens a support ticket regarding a transaction, payout, or dispute, FlowAssist queries internal payment ledgers and clearing logs, reconstructs the full end-to-end payment lifecycle timeline, checks regulatory constraints (PSD2 SCA, AML/KYC reserve holds), and drafts a cited response with direct transaction hyperlinks in the Zendesk sidebar for the human agent to review, edit, and send.

**Trust level per step:**  
- *Data Retrieval & Lifecycle Reconstruction:* **L4** (autonomous read-only querying of ledger and clearing logs).
- *Grounding & Match Verification:* **L4** (automated dual-LLM evaluator scores factual consistency; drops to context-only if confidence < 0.95).
- *Draft Formulation:* **L2** (draft displayed strictly in the internal agent sidebar).
- *Merchant Communication & Fund Actions:* **L1 (Human Only)** (human payment specialist approves/edits every single outbound message; copilot has zero write access to funds).

**One thing it must never do:**  
It must **never** send an outbound communication directly to a merchant, **never** execute or promise any fund transfer, refund, or settlement release, and **never** match or disclose transaction details without a cryptographically verified merchant account ID match (preventing cross-tenant data leakage).

**Why it is a product decision:**  
The Head of Product, VP of Customer Operations, and Chief Compliance Officer (CCO) must collectively decide whether to ship FlowAssist. While an autonomous L3/L4 bot could theoretically deflect tickets at lower labor cost, in B2B payments **"a wrong transaction match is worse than no draft."** Providing inaccurate wire status or disclosing another merchant’s settlement data violates banking secrecy and PSD2 regulations, risking severe regulatory sanctions (ACPR/BaFin) and immediate loss of enterprise customer trust. The product decision is to deliberately enforce an **L2 copilot architecture with an automated grounding evaluator gate**, optimizing agent productivity while maintaining zero-defect human accountability.

## Checklist (all seven must be ticked)
- [x] A named company type, a ticket volume and a team size (PayFlow B2B, 800 merchants, 12,000 tickets/month, 18 agents)
- [x] A pain expressed as a cost (40% investigation time = €414,720/year in wasted handling labor + €35,000 SLA penalties)
- [x] A do-nothing baseline (4% natural productivity gain = €57,600/yr; requires 4 new hires / €220k to absorb 25% volume growth)
- [x] One job in one sentence (When [trigger], the agent [does], producing [outcome])
- [x] A trust level per step, at least one below L4 (L4 retrieval, L4 evaluator, L2 draft, hard L1 human approval on customer-facing send)
- [x] One thing it must never do (Never message customers directly, never move funds, never leak cross-tenant transactions)
- [x] A real decision: someone must decide whether to ship it (Head of Product & CCO weigh AHT savings against transaction match liability)
