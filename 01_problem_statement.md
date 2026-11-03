# 01 — Problem statement

**Team:** PayFlow AI Product Team (Lenny Santus, Anthony Rascle, Antoine Rabeau, Benjamin Caujolle & Colin Sibieude) · **Agent:** P2 — Agent-assist copilot for a fintech (B2B payments) · **Last updated:** 16 October 2026

> Every number says where it comes from: **measured**, **analogy** (a comparable, with its source) or **guess** (and how you will test it).

## 1. The problem in one sentence
Tier-1 payment operations specialists at PayFlow B2B (a European fintech serving 800 merchant accounts with 12,000 support tickets a month) spend 40 % of their handling time (7.2 minutes out of an 18-minute AHT) manually querying transaction ledgers, bank clearing gateways (SEPA/SWIFT GPI), and dispute portals before drafting a reply, costing ~€415k a year in wasted investigation labor and driving a 4.5-hour median first response time; today they switch across six admin tabs, copy-paste transaction IDs into SQL consoles, and draft responses from memory while merchants wait. Success looks like reducing average handling time (AHT) by 30 % (from 18.0 to 12.6 minutes) across payment tracing, dispute, and compliance tickets at constant quality (internal QA score ≥ 92 % and zero cross-tenant data leaks) within 12 weeks of deployment.

| Number in the sentence | Value | Measured / analogy / guess | Source or test |
|---|---|---|---|
| Merchant accounts | 800 | Measured | Active enterprise and marketplace merchant accounts in CRM (Q3 2026). |
| Monthly ticket volume | 12,000 | Measured | Zendesk ticket logs averaged over the trailing 12 months (144,000 tickets/yr). |
| Share of handling time spent investigating | 40 % | Measured | Time-and-motion study on 250 sampled tickets tracked via screen-recording in June 2026. |
| Baseline Average Handling Time (AHT) | 18.0 min | Measured | Median handling time recorded across tier-1 Zendesk payment queues. |
| Investigation time per ticket | 7.2 min | Measured | 40 % × 18.0 min baseline AHT. |
| Median first response time | 4.5 hours | Measured | Zendesk SLA monitoring metrics over Q1–Q3 2026. |
| Cost of investigation labor | €414,720 / yr | Analogy | 144k tickets × (7.2 min / 60 min) × €24.00/hr loaded agent wage (derived from €55k annual loaded cost). |
| Fully loaded cost per ticket | €10.00 | Analogy | Session 2 slide benchmark (€8–€15 all-in human ticket cost for B2B SaaS/fintech) and Paylio class exercise. |
| Target AHT reduction | 30 % (to 12.6 min) | Guess | Tested on 200 payment tracing tickets in the Session 4 prototype (validating the hurdle flip point ≥ 41.2 % on Category 1); measured via agent-level A/B test in Session 6. |
| Quality threshold (QA score) | ≥ 92 % | Measured | Existing internal Support QA rubric (accuracy, tone, compliance citation, policy adherence). |
| Rollout timeframe | 12 weeks | Guess | Staged quarterly ramp: pilot (Q1) to full 18-agent deployment (Q4). |

### 1.1 Persona & User Journey Map (S1 Slide 19)
- **Persona:** Karim, 27 — Tier-1 Payment Operations Specialist at PayFlow B2B.
  - *Goal:* Resolve 25–30 tickets/day at Support QA score ≥ 92 % and zero compliance breaches.
  - *Pain:* 40 % of his day is lost hunting through 6 disconnected backend databases (PostgreSQL ledger, SEPA XML logs, SWIFT GPI, card dispute portal, KYC flags).
  - *Tools:* Lives in Zendesk, Slack, internal SQL consoles, and clearing admin portals.
  - *Fear:* Being blamed for an erroneous transaction match or leaking another merchant's financial data to a customer (Moffatt v. Air Canada precedent).
- **Karim’s Day — Where the pain sits across the 18-minute journey:**
  1. *Read incoming ticket (1.5 min):* Extract ambiguous date, gross amount, and counterparty metadata.
  2. *Search ledgers & clearing logs (5.7 min) — [CORE PAIN]:* **FlowAssist L4 Retrieval lands here** (auto-queries ledgers in < 2 seconds).
  3. *Draft response & paste transaction URLs (4.8 min) — [CORE PAIN]:* **FlowAssist L2 Drafting lands here** (pre-populates Zendesk sidebar draft).
  4. *Check compliance & scheme rules (2.5 min):* **FlowAssist L4 Grounding Evaluator checks here** (validates PSD2/SCA flags and confidence score).
  5. *Review, edit & send (2.0 min):* **Human L1 accountability** (Karim reviews citations, adjusts tone, and clicks send).
  6. *Ticket categorization & CRM logging (1.5 min):* Automated tag suggestion.

### 1.2 Stakeholder Map (S1 Slide 26)
| Quadrant | Stakeholders | Strategy & Key Concerns |
|---|---|---|
| **Manage Closely** *(High Power, High Interest)* | Head of Payment Operations · CFO | Support SLA performance, AHT reduction (-30 %), team burnout, business case ROI (€141k net value vs €125k hurdle). |
| **Keep Satisfied** *(High Power, Low Interest)* | Chief Compliance Officer (CCO) · DPO · Legal | EU AI Act compliance (limited risk / Art. 50), GDPR Art. 6 legal basis, zero cross-tenant leakage, strict PCI-DSS VPC data boundary. |
| **Keep Informed** *(Low Power, High Interest)* | Tier-1 Support Specialists (Karim & team) | Zendesk UI ergonomics, draft grounding accuracy, trust in citations, no fear of replacement (L2 copilot empowers them). |
| **Monitor** *(Low Power, Low Interest)* | Enterprise Merchants & B2B Marketplaces | Speed and clarity of "Where is my money?" reconciliation inquiries, SLA compliance, cash flow predictability. |

## 2. Problem tree — from symptom to cause
- **Symptom** (what people complain about):
  Merchants complain that urgent "Where is my money?" reconciliation questions take over 4 hours to get answered, delaying their daily cash flow reconciliation. Support agents complain of cognitive exhaustion, high stress during peak trading days, and frustration with having to consult 6 different internal tools to answer a single routine inquiry.
- **Problem** (what is actually going wrong):
  Agents spend 7.2 minutes per ticket manually gathering, correlating, and interpreting fragmented transaction data across separate backend systems (core SQL ledger, SEPA XML clearing logs, SWIFT GPI tracker, Stripe/Adyen gateway feeds, and KYC/AML compliance tables) before they can begin composing an accurate customer reply.
- **Root cause** (5 Whys):
  1. *Why do agents take 18 minutes to resolve a ticket?* Because 40 % of handling time is spent reading transaction history, checking clearing webhooks, and searching past tickets before typing a single sentence.
  2. *Why do they have to search so many places?* Because payment data is fragmented across 4 disparate infrastructure services: the core double-entry accounting ledger, the bank clearing gateway, the card scheme dispute console, and the KYC/compliance database.
  3. *Why isn't this data consolidated into a single merchant view?* Each backend system was built as an independent microservice with its own database, API schema, and internal admin UI, with no unified presentation layer for support.
  4. *Why can't simple SQL macros or deterministic rules solve it?* Because merchant inquiries arrive in unstructured natural language with incomplete or ambiguous references ("our €14,200 wire from Tuesday morning", "buyer claims double charge on order #8921"), requiring semantic entity extraction, time-window matching, and fee deduction calculations rather than exact-match key lookups.
  5. *Why can't an autonomous customer-facing bot answer directly?* Because financial transactions carry legal liability and banking secrecy obligations: a wrong transaction match is worse than no draft. Revealing another merchant’s data or misconfirming an un-cleared wire exposes PayFlow to regulatory fines (GDPR, PSD2) and financial dispute losses.
- **What would fix the cause:**
  An agent-assist copilot that ingests the incoming merchant ticket, extracts transaction parameters, queries the backend ledgers via read-only APIs, reconstructs the transaction lifecycle timeline, checks regulatory flags (PSD2 SCA, AML holds), scores groundedness with an automated evaluator, and generates a pre-formatted draft reply with transaction links directly in the agent's Zendesk sidebar.
  - **Nature of the fix:** **AI (LLM Orchestration + RAG + Grounding Evaluator)** paired with an **operational process change** (agent workflow in Zendesk sidebar). It cannot be fixed by documentation alone (the data is live and transactional), nor by a rule (unstructured natural language requires semantic parsing), nor by a customer-facing bot (unhedged error cost violates financial compliance).

## 3. Is AI the right tool?
| Question | Our answer |
|---|---|
| **Is there a rule that solves 80 % of it?** | **No.** Static rules and Zendesk macros resolve only ~15 % of tickets (generic API documentation links or public banking holiday schedules). 85 % of tickets require extracting vague payment metadata from merchant text (dates, gross amounts, recipient names, missing reference codes) and dynamically joining multi-table ledger logs. Deterministic keyword matching fails when amounts differ due to interchange fee deductions or foreign exchange conversions. |
| **Is it a prediction / generation problem, or an organisational decision?** | **It is an extraction, prediction, and generation problem.** The copilot must extract transaction entities, predict the matching ledger transaction UUID, and generate a clear, professional explanation of the clearing stage. The underlying business rules (settlement cutoff times, Visa/Mastercard dispute timelines, PSD2 Strong Customer Authentication requirements) are deterministic legal frameworks; the AI simply retrieves the facts and drafts the text. |
| **Do we have the data — which, how much, who owns it?** | **Yes, 100 % owned internally within PayFlow's VPC.** 144,000 historical Zendesk tickets with verified agent resolutions (12 months of logs), PostgreSQL core accounting ledger tables, banking gateway clearing webhooks (SEPA camt.053/camt.054, SWIFT MT103), and KYC compliance flags. Legal basis: GDPR Art. 6(1)(b) (contractual necessity to process payments and handle support). Governed by internal Data Engineering and Payment Ops teams. |
| **What does one error cost — and who pays it?** | **Between €15 and €250+ per error, paid by PayFlow B2B.** If an AI draft provides incorrect clearing information, the merchant re-opens the ticket, requiring Tier-2 senior engineering escalation (€15–€25). If an incorrect dispute deadline is provided, the merchant loses chargeback rights (€90–€150 liability). If tenant A's transaction data is leaked to tenant B, PayFlow faces catastrophic regulatory sanctions under GDPR Art. 33/34 and banking secrecy laws. This unhedged tail risk is precisely why the agent operates at Trust Level L2: a human specialist reviews every draft, and an automated Grounding Evaluator drops low-confidence drafts (< 0.95) to "context-only". |

**Level chosen:** **GenAI Agent-Assist Copilot (Trust Level L2)**  
- *Why not Rules?* Rules cannot parse conversational merchant emails with partial, ambiguous payment details or reconcile multi-hop banking clearing logs.
- *Why not Classical ML?* Supervised classification (e.g. BERT/XGBoost) can categorize ticket intent (e.g. `intent: payment_delay`), but cannot synthesize an end-to-end multi-source narrative, extract exact clearing timestamps, or draft an individualized reply with transaction deep-links.
- *Why not Autonomous Agent (L3/L4)?* Autonomous customer-facing execution creates unhedged financial and legal liability: in B2B payments, **a wrong transaction match is worse than no draft.** Giving the agent autonomous sending rights violates compliance and risks severe reputational damage.

## 4. Why this agent — the four selection questions
| Criterion | Our answer, one line |
|---|---|
| **High frequency** — is the work done every day or every hour? | **Yes.** 12,000 tickets/month (~400 tickets/day), handled continuously by 18 support specialists across all business hours. |
| **Bounded decision space** — can we list its tools and outcomes on one slide? | **Yes.** Exactly four read-only API tools (`get_merchant_account`, `search_ledger`, `get_clearing_status`, `get_compliance_holds`) and two possible UI outcomes (Grounded Draft vs Context-Only Card). Zero funds write access. |
| **Measurable success** — can we say in one sentence whether it succeeded on one ticket? | **Yes.** Success on a ticket means the agent accepted the draft (edit distance < 30 %), handling time was reduced by ≥ 30 %, the merchant did not reopen the ticket within 7 days, and QA score is ≥ 92 %. |
| **Recoverable failure** — if it is wrong, is the damage limited and reversible? | **Yes.** Because the copilot never sends the message directly to the customer (L2), errors are caught and corrected by the human specialist before leaving PayFlow. |

## 5. Press release (Working Backwards)
*One paragraph, dated launch day: who it is for, what changed for them, one number, one customer quote (Colin Bryar & Bill Carr method, Session 1).*

**PARIS / LONDON — November 18, 2026** — PayFlow B2B, the European payment infrastructure platform serving 800 enterprise marketplaces and B2B SaaS platforms, today announced the production rollout of **FlowAssist**, an intelligent agent-assist copilot embedded within its payment operations center that cuts average support handling time from 18.0 to 12.6 minutes across 144,000 annual merchant inquiries. Developed to eliminate manual multi-database investigation across fragmented SEPA, SWIFT, and card ledgers, FlowAssist automatically reconstructs end-to-end payment lifelines with verifiable audit citations, enabling human specialists to resolve urgent liquidity inquiries in under 15 minutes. *"We used to wait half a business day to track cross-border supplier disbursements delayed in intermediary clearing,"* said Marc Dupont, CFO of B2B procurement network Synapse Commerce; *"with PayFlow's FlowAssist copilot, their support specialists provide exact SWIFT GPI clearing milestones and debit confirmations in 15 minutes flat, with full audit receipts attached directly to the message."*

## 6. What would have to be true?
| # | Hypothesis | Measured / analogy / guess | How we will test it | Session |
|---|---|---|---|---|
| 1 | **Deterministic Transaction Matching:** At least 75 % of "Where is my money?" tickets contain sufficient extractable entities (amount, date window, counterparty IBAN, or reference) to match the unique transaction ID in the core ledger with ≥ 99 % recall. | Guess (supported by exploratory 50-ticket audit) | Run entity extraction and deterministic ledger querying over an offline golden dataset of 200 historical tickets in the Session 4 prototype (`/prototype` & `/evals`). | S4 prototype |
| 2 | **Evaluator Precision (Circuit Breaker):** An automated LLM-as-a-judge Grounding Evaluator can detect hallucinations and transaction mismatches with ≥ 98 % precision, successfully suppressing false drafts down to "Context only". | Guess | Benchmark the evaluator model against 200 curated draft pairs (including 40 synthetic adversarial ledger mismatches and edge cases) in Session 5 metrics. | S5 metrics |
| 3 | **Productivity & Quality Equilibrium:** Support specialists equipped with FlowAssist reduce average handling time by at least 30 % (≥ 5.4 minutes saved per ticket) without degrading customer QA scores (≥ 92 %) or increasing 7-day ticket reopen rates (< 5 %). | Analogy (Klarna support benchmark: 3.2 min vs 11 min baseline; Stripe support assist) | Execute a 4-week agent-level randomized controlled trial (A/B test: 9 copilot agents vs 9 control agents) using a difference-in-differences design in Session 6. | S6 A/B protocol |

## 7. Do-nothing baseline
What happens in 12 months if nobody builds anything?
- **Natural efficiency gain:** Support agents gradually build personal macro collections, improve their query speed in PostgreSQL consoles, and update internal Notion documentation. This yields a modest historical productivity gain of approximately **4 % per year** (~€57,600/year in labor efficiency).
- **Merchant volume expansion:** PayFlow's merchant customer base is projected to grow from 800 to 1,000 accounts (+25 % YoY), driving monthly support volume from 12,000 to 15,000 tickets/month (180,000 tickets/year).
- **Headcount and financial penalty:** Without automation, maintaining the current 18-minute AHT and 4.5-hour response SLA under 15,000 monthly tickets requires hiring **4 additional Tier-1 agents**, adding **€220,000/year** in loaded payroll and tooling costs.
- **Enterprise SLA risk:** High volume peaks during month-end billing cycles already trigger SLA breaches with tier-1 enterprise merchants, resulting in contract penalties of ~€35,000/year. Without an automated copilot, SLA breaches will increase by an estimated 40 %.
- **Burnout and turnover:** Payment support operations suffer from a 30 % annual staff turnover rate due to repetitive database hunting and high stress. Doing nothing perpetuates recruiting costs, 6-week onboarding ramp times, and institutional knowledge loss.
