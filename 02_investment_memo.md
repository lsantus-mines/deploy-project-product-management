# 02 — Investment memo (one page)

**Recommendation:** CONDITIONAL GO on handling time reduction ≥ 41.2 % on 200 payment tracing tickets and grounding evaluator precision ≥ 98 % in the Session 4 prototype.

> Line one is the decision. Everything below is evidence for that line. Same base case as `02_sizing.xlsx`.

| €/year, year 1 | Pessimistic | Base | Optimistic | Expected value |
|---|---|---|---|---|
| Net annual value | -€59,828 | €141,340 | €434,862 | €159,810 |
| Probability | 20 % | 60 % | 20 % | — |
| Do-nothing (value of current process improving on its own) | €32,130 | €57,600 | €96,600 | €60,306 |
| Next-best project: Merchant Self-Serve Dispute & Reconciliation Portal (the hurdle) | €100,000 | €125,000 | €145,000 | €124,000 |

## 1. How much?
The base-case net annual opportunity is **€141,340** in Year 1 (scaling to **€305,500/year** at mature steady-state adoption), derived bottom-up across PayFlow's 144,000 annual tickets (12,000/month across 800 merchant accounts) handled by 18 Tier-1 agents with a loaded cost of €10.00/ticket:
1. **Payment Tracing & Reconciliation** (50 % volume, 75 % automatable, 48 % handling time saved, 46.25 % Year-1 adoption ramp): yields 11,988 deflected ticket equivalents → **€114,902** net variable contribution (€119,880 gross savings − €4,496 error cost − €482 AI token costs).
2. **Disputes & Chargebacks** (30 % volume, 60 % automatable, 32 % time saved, 46.25 % Year-1 adoption ramp): yields 3,836 deflected ticket equivalents → **€27,850** net variable contribution (€38,362 gross savings − €10,358 error cost − €154 AI token costs).
3. **KYC & PSD2 Regulatory Holds** (20 % volume, 50 % automatable, 25 % time saved, 46.25 % Year-1 adoption ramp): yields 1,665 deflected ticket equivalents → **€11,588** net variable contribution (€16,650 gross savings − €4,995 error cost − €67 AI token costs).
4. **Other Strategic Value:** **€65,000/year** from avoiding 35 contractual enterprise SLA breach penalties (€35,000 at €1,000/breach) and retaining at-risk enterprise merchants via sub-15-minute dispute resolution (€30,000 gross margin retained).
5. **Fixed & Semi-Fixed Costs:** **€78,000/year** (Integration amortised over 3 years at €20,000/yr; golden eval-set maintenance at €22,000/yr; 0.3 FTE payment specialist L2 oversight at €16,500/yr; observability & on-call at €12,000/yr; and 3 model re-evaluations at €7,500/yr).

**Data Sourcing:**
- **Measured:** 12,000 monthly tickets, 800 merchant accounts, 18 agents, and category volume shares (50 % / 30 % / 20 %) from 12-month Zendesk logs.
- **Analogies:** €10.00 fully loaded human ticket cost (industry standard €8–€15 for B2B fintech support; matches Paylio benchmark); €0.035 API token cost per conversation (Claude 3.5 Sonnet / GPT-4o-mini); 4 % annual natural do-nothing efficiency gain.
- **The one guess that matters:** The **48 % handling time saved on Payment Tracing tickets**. Because Category 1 represents 50 % of volume, a 10 % swing in its deflection moves net value by ~€24,000/year.

## 2. How sure?
Weighting three scenarios (Pessimistic: 20 %, Base: 60 %, Optimistic: 20 %) yields an **Expected Value (EV) of €159,810/year**, beating the €125,000 hurdle by **+€34,810** and the do-nothing baseline by **+€102,210**.
- **The assumption that flips the decision (Flip Point):** Reading down the Decision tab sensitivity table (varying Category 1 deflection from 0.30 to 0.75), Net Annual Value is **€98,251 at 0.30 deflection** (below the hurdle by €26,749) and **€134,158 at 0.45 deflection** (clearing the hurdle by €9,158). The decision flips at exactly **41.2 % handling time saved on Payment Tracing tickets**.
- **Prototype De-risking:** The Session 4 prototype (`/prototype` and `/evals`) will test FlowAssist against 200 real historical payment tracing tickets with manual time-and-motion auditing. If the measured handling time reduction is ≥ 41.2 % and grounding precision is ≥ 98 %, we immediately greenlight full engineering integration.

## 3. What if we're wrong?
- **Dominant Cost Lines:** Inference token costs are negligible (**€704/year** in Base). Fixed engineering, evaluation, and human supervision dominate (**€78,000/year**). 
- **Cost of Error (Priced Tail):** We explicitly price **€19,848/year** in expected error costs across categories (€4,496 tracing + €10,358 disputes + €4,995 KYC/holds).
- **The Governance Tail Risk:** The critical catastrophic risk is not operational rework, but a **cross-tenant data breach or transaction mismatch** on a KYC or clearing ticket (Category 3). Disclosing Merchant A's settlement figures or bank details to Merchant B is a severe breach of banking secrecy and GDPR Art. 33/34, risking regulatory sanctions from banking authorities (ACPR/BaFin) and GDPR fines up to 4 % of global turnover.
- **Risk Owner:** Owned by the **Chief Compliance Officer (CCO)** and **Data Protection Officer (DPO)**. To mitigate this tail, FlowAssist implements an automated dual-LLM Grounding Evaluator: any draft scoring below a 0.95 confidence threshold on entity matching is automatically suppressed into a read-only "Context Card", preventing hallucinated drafts from ever reaching the agent's editor.

## 4. Compared to what?
- **Do-Nothing Trajectory:** Support specialists naturally improve by 4 % per year through manual macros and Notion guides (€57,600/year efficiency gain). However, merchant volume is expanding by 25 % YoY (+3,000 tickets/month), which would force hiring 4 additional Tier-1 agents (+€220,000/yr in fixed payroll). FlowAssist EV outperforms do-nothing by **+€102,210/year** and scales smoothly without proportional headcount growth.
- **Next-Best Project (The Hurdle):** "Merchant Self-Serve Dispute & Reconciliation Portal" (automated CSV exporter and webhook builder), delivering an estimated €125,000/year net value. FlowAssist EV beats this hurdle by **+€34,810/year**.
- **Downside Risk:** The pessimistic case yields **-€59,828/year**, failing to clear the €100,000 hurdle. This justifies our **CONDITIONAL GO**: we will not commit capital to full production integration until the S4 prototype proves handling time savings ≥ 41.2 %.

## 5. Build, buy or orchestrate?
**We orchestrate because proprietary payment ledgers and strict PCI-DSS/GDPR banking residency require keeping transaction retrieval inside our VPC, while leveraging state-of-the-art LLMs via enterprise zero-data-retention APIs.**  
Weighted scores from the `Build or buy` tab: **Build 3.15 · Buy 2.15 · Orchestrate 4.35**.  
- *Why Buy fails (2.15):* Off-the-shelf support bots (e.g. Intercom Fin at €0.92/resolution) appear €34,114 cheaper on paper in Year 1 (€16,090 vendor fees vs €50,204 internal fixed amortisation & evaluation), but cannot query private double-entry accounting ledgers or SEPA/SWIFT clearing webhooks behind our banking firewall without custom middleware. Furthermore, SaaS vendors offer zero contractual indemnity for banking secrecy violations or costly financial transaction mismatches.
- *Why Pure Build fails (3.15):* Training custom proprietary models from scratch requires 9–12 months of ML engineering and high infrastructure overhead with zero competitive advantage over modern foundation models.
- *Why Orchestrate wins (4.35):* Building a proprietary RAG retriever and Grounding Evaluator over internal databases while querying enterprise LLM APIs (Claude 3.5 Sonnet / GPT-4o-mini with zero data retention) allows deployment in 8 weeks, full VPC data isolation, and total auditability.
- *Condition that would change our mind:* We would switch to **Buy** only if an enterprise fintech vendor launches an on-premise, PCI-DSS certified copilot connector with pre-built SEPA/SWIFT parsers and contractual legal indemnity against transaction mismatches priced below €0.40 per resolution.

*Sources: 1) PayFlow internal Zendesk ticket logs & PostgreSQL transaction ledger (2025–2026, 144k tickets). 2) Klarna AI assistant press release (Feb 2024) & Bloomberg analysis (May 2025). 3) Stanford HAI AI Index Report 2025. 4) Intercom Fin pricing & resolution economics (2025). 5) Colin Bryar & Bill Carr, Working Backwards (2021). 6) Kohavi, Tang & Xu, Trustworthy Online Controlled Experiments (2020).*
