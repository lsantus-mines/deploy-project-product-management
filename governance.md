# Governance — our living file

> Created for Assignment 1, one line added every session. One question at the oral is drawn from this file.  
> Answers are provisional: write what you know today, and mark what you still have to check.

## Session 1 — the six questions
| # | Question | Our answer (provisional) | To check with |
|---|---|---|---|
| 1 | **EU AI Act:** which risk tier is our agent in, and why? (minimal · limited — transparency: tell the user it is an AI · high-risk · prohibited) | **Limited risk (transparency obligations under Art. 50).** FlowAssist is an internal agent-assist copilot (Trust Level L2) assisting human support agents; it does NOT make automated decisions granting or denying access to essential financial services (credit, insurance, or account opening), which avoids the High-Risk tier (Annex III). We must log internal AI usage, maintain an AI transparency notice for agents, and ensure auditability. | Legal Counsel / Compliance Officer (confirm interpretation with ACPR/BaFin guidelines) |
| 2 | **Data:** whose data does it use, and on what legal basis? (GDPR art. 6; what the B2B contract allows) | **Merchant enterprise account and payment transaction data.** Legal basis: **GDPR Art. 6(1)(b)** (performance of the B2B merchant payment processing contract) and **Art. 6(1)(f)** (legitimate interest for support optimization and fraud triage). FlowAssist queries data stored within PayFlow's AWS EU-West-3 (Paris) VPC. Model API calls to LLM providers (Anthropic Claude 3.5 Sonnet / OpenAI) enforce zero data retention (ZDR) and zero model training on customer payloads. Strict cryptographic tenant-isolation (row-level security on `merchant_id`) prevents cross-tenant data leakage. | Data Protection Officer (DPO) & Information Security (CISO) |
| 3 | **Accountability:** who is accountable when it is wrong — and where is the human? | **The human Tier-1 payment operations specialist who reviews, edits, and sends the response is operationally accountable.** The **Head of Payment Operations** owns overall support SLA and answer quality. The **VP of Product** owns model performance and guardrails. The copilot operates strictly at Trust Level L2: it cannot send messages, execute fund transfers, or modify ledger records autonomously. "The AI made a mistake" is explicitly rejected as an operational or legal defense (Moffatt v. Air Canada precedent). | Head of Payment Operations & VP Product |
| 4 | **Never:** what must it never do? (our first guardrail) | **The agent must NEVER send an outbound message directly to a merchant, NEVER execute or authorize any monetary transfer, refund, or settlement release, and NEVER disclose transaction details without a cryptographically verified merchant account ID match (preventing cross-tenant data leaks).** | VP Engineering & Payment Ops QA Lead |
| 5 | **Explainability:** explainable to whom — the customer, the support agent, the auditor? | **To all three, at different levels of abstraction:**<br>1) *The Support Agent:* The Zendesk sidebar displays exact source citations with direct hyperlinks to internal transaction UUIDs, clearing house batch IDs, and database timestamps, plus a Grounding Confidence Score.<br>2) *The Merchant / Customer:* The drafted text explains the payment status in clear, human-readable plain language (e.g. "funds cleared French SEPA interbank clearing at 14:15 CET, pending beneficiary bank credit") without internal database jargon.<br>3) *The Auditor / Regulator (ACPR/BaFin):* Complete immutable JSON audit trail logging: incoming ticket, retrieved ledger records, prompt template, raw LLM draft, grounding evaluator score, agent edit diff, and final approved message with agent ID. | Payment Operations Lead & Internal Audit |
| 6 | **The people it cannot serve:** what happens to them? | **Edge cases and ungrounded queries are automatically escalated to human Tier-2 specialists.** If the Grounding Evaluator score is below 0.95 (ambiguous entities, multiple conflicting transactions, or unparseable inquiries), the copilot suppresses the draft and displays a "Context Only — No Draft Generated" banner. Complex dispute arbitration, suspected fraud syndicates, or legal subpoena requests bypass the copilot entirely via automated Zendesk priority routing. Multilingual inquiries (French, German, English) are handled through standardized English ledger normalization. | Tier-2 Escalations Manager |

## Session 2 — the cost of error
- **Which cost-of-error line is a legal or reputational risk, not just money?**  
  **Category 2 (Dispute deadlines & scheme rules) and Category 3 (KYC, Onboarding & PSD2 Regulatory Holds / Cross-tenant data leakage).**  
  While an error in Category 1 (Payment Tracing) merely causes merchant annoyance and agent re-investigation labor (~€15–€25/ticket), an error in Category 3 carries existential legal and regulatory exposure:
  1. *Cross-Tenant Data Leakage:* Displaying or sending Merchant A the transaction details, customer names, or bank account numbers of Merchant B violates banking secrecy laws and GDPR Art. 33/34. This triggers mandatory 72-hour regulatory breach notifications, potential GDPR fines up to 4 % of global annual turnover, and acute loss of enterprise merchant trust.
  2. *Regulatory Hold Misinformation:* Misinforming a merchant regarding PSD2 Strong Customer Authentication (SCA) exemptions or AML compliance reserve freezes can lead to wrongful fund retention claims, regulatory audits by financial supervisory authorities (ACPR in France, BaFin in Germany, FCA in the UK), and jeopardy of PayFlow’s payment institution license.
  3. *Missed Dispute Deadlines:* In Category 2, hallucinating a false card network dispute submission window (e.g. telling a merchant they have 30 days when Visa card scheme rules enforce a strict 14-day cutoff) causes the merchant to permanently forfeit chargeback rights, generating direct financial liability and contractual litigation.
- **Who in the company owns that risk?**  
  - **Regulatory & Data Compliance:** The **Chief Compliance Officer (CCO)** and the **Data Protection Officer (DPO)** own the regulatory liability, reporting to financial supervisory authorities, and GDPR breach management.  
  - **Operational & Scheme Liability:** The **Head of Payment Operations** owns the QA protocol, agent training, and dispute submission timelines.  
  - **Technical Guardrail Enforcement:** The **VP of Engineering** and **AI Product Lead** own the dual-LLM Grounding Evaluator, tenant-isolation query firewalls, and automated circuit breakers that suppress unverified drafts.

## Session 3 — data and trust levels · 2 November 2026

### Evidence boundary and corrections to S1/S2
P2 supplies the educational scenario (800 merchants, 12,000 monthly tickets, 40% investigation time). The repository contains no PayFlow ticket exports, ledger, time study, signed contract or provider deployment evidence. Earlier “measured” internal-data statements are scenario assumptions, not verified research. S3 uses **only synthetic data**. The Paylio starter is a separate class example and is not FlowAssist evidence.

The following updates supersede earlier design proposals for this MVP: a model score never authorizes a tenant/transaction match; retrieval is read-only and tenant-scoped with human match confirmation; customer sending is **person only**, not L1; dispute/KYC advice is out of scope. A second LLM is an unproven checker, not an isolation guarantee. ZDR, EU hosting and a lawful basis are requirements to verify before live use, not properties demonstrated here.

### Six-question data audit
| # | Question | Answer for S3 and proposed live system | Source type | To check with |
|---|---|---|---|---|
| 1 | Provenance | 20 AI-generated synthetic inputs, explicit fictional ledger snapshots and policy fixtures, created 2 Nov 2026. No actual customer data. Future ticket/ledger/clearing records need system owner, collection timestamp and lineage per record. | Repository inspection; future access is a guess | Data Engineering + Ops |
| 2 | Volume & labels | 50 development rows (including the original 20 S3 seeds), expected actions proposed by AI and **not yet human-labelled**. Two team members must independently check labels and references before freeze. The 144k historical tickets in S1/S2 are unavailable. | Counted development rows; scenario volume | Ops QA + independent team reviewers |
| 3 | Coverage | Seed covers EN/FR/DE plus unsupported PT; EUR SEPA, USD SWIFT; SMB/Enterprise; routine, ambiguous and critical cases. Plans/regions are explicit row metadata; population shares are unknown. No claim of representative segment performance. | Synthetic design choices | Ops + language reviewers |
| 4 | Rights | Synthetic coursework has no customer-data rights grant. Future processing needs purpose, controller/processor mapping, DPA, provider no-training/retention terms and approved transfers. Art. 6(1)(b) applies only where necessary for a contract with the data subject; a B2B corporate contract alone does not establish this for every contact/counterparty. Assess Art. 6(1)(f) necessity/balancing where appropriate; no assumed approval. | Proposed legal interpretation, validation pending | DPO / Legal |
| 5 | Leakage | No ticket reuse across tenants. Backend session supplies merchant ID; access check and row-level filter occur **before retrieval**. Cache keys include tenant and scope; prompts, citations and logs retain this boundary. Negative tests include foreign reference and forged tenant instruction. Split evaluation from prompt development by scenario family and near-duplicate check. | Design; not implemented security evidence | CISO + Engineering |
| 6 | Freshness | Each snapshot carries event/fetch time and version; provisional maximum age 5 min. Missing/stale/conflicting data suppresses draft. Version policy fixtures and rerun after changes. Production freshness/SLA must be agreed with clearing owners. | Guess to test; fixture timestamps explicit | Clearing owner + Ops |

### Purpose, minimisation and retention
Purpose: answer an assigned merchant's payment-tracing ticket with evidence and human approval. No training, marketing, employee scoring or unrelated profiling. GDPR Article 5 requires purpose limitation, data minimisation and storage limitation; proposed durations below are design choices, not statutory periods. [GDPR Articles 5–6](https://eur-lex.europa.eu/legal-content/ENG/ALL/?uri=celex%3A32016R0679).

| Artifact | Proposed retention / control | Owner |
|---|---|---|
| Synthetic fixtures and code | Course repository lifecycle; no personal payment data | Team |
| Interview notes | Anonymised, only with permission; delete within 30 days after final assessment; no raw audio by default | Research lead |
| Live retrieval context | Request memory only, clear at completion; no shared raw-result cache in MVP | Engineering |
| Raw prompts / model replies | Do not persist by default; redact secrets and personal identifiers before API use | Engineering + DPO |
| Minimized live audit metadata | Proposed 90 days; ticket ID, actor, policy/model/source versions, gate reasons, approval event; restricted append-only store | Ops + CISO, DPO approval |
| Original support / financial records | Existing separately approved source-system schedule; no new full ledger copy | System owner + Legal |

No real-data call until provider terms, retention controls, sub-processors, hosting/transfers, and access paths have been checked. Full PAN, credentials and unmasked banking identifiers are excluded. Anonymisation claims require re-identification assessment; masking alone is not anonymisation.

### Customer isolation and known gaps
Server-side assigned-agent authorization → tenant-constrained parameterized query → authorized source set → redaction → model prompt. Recheck tenant and transaction identity on citations and draft insertion. Index namespace and any cache key include `merchant_id`; no global historical-ticket search. Failed auth returns empty context and an access-denied state. A model “ignore tenant” instruction can never change scope. Test unauthorized references, mixed-tenant results, stale cached responses and log access before enabling live use.

Gaps: tiny synthetic sample; no real distributions, accented German/colloquial French review, non-EU rails, unsupported languages, unusual currency precision, complex multi-party payments or live permission tests. PT goes to a person; dispute/fraud/KYC goes to specialists in every language. Report failures and fallbacks by language, plan, rail, region and severity; do not claim fairness or accuracy from one or two cases.

### Trust level per step
| Step | Level / authority | Reason |
|---|---|---|
| Intent and entity suggestions | L1 | Unstructured or hostile text may mislead; session establishes identity |
| Tenant-scoped read-only candidate retrieval | L3 within assigned ticket; sampled Ops review, person confirms selected match | Financial matching errors are costly; deterministic authorization is mandatory |
| Timeline / reply drafting | L2 | Every claim cites approved evidence, human checks |
| Policy / grounding | Rules automatically block; L2 specialist validates passing content | Model score is not a safety proof; disagreement fails closed |
| Review, edit, send | Person only | Customer communication and liability remain with the organization and human approver |
| Audit metadata | L4 bounded append-only write | No financial/customer action, limited data scope |
| Escalation | Person action, safe context packet | Agent can always return to manual tools |

Ops Lead can disable drafts immediately; Engineering revokes generation while manual support continues. Any tenant exposure, wrong-transaction disclosure or attempted outbound/fund write is a stop event. DPO/CCO assesses notification duties from the facts; S1/S2's blanket automatic-notification wording must not replace incident assessment. No production compliance certification is claimed.

**AI Act status:** internal decision support for tracing, with no creditworthiness or eligibility decision; final classification and applicable transparency obligations require Legal review of actual intended use. An “AI-assisted draft” label is included for operators. The earlier blanket “limited risk under Article 50” conclusion is provisional, not a legal determination. [European Commission, Article 50 transparency guidance](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act).

### S3 v2 design decisions — 3 November 2026
Decisions D01–D05 are team desk analysis, not participant evidence; see `03_user_research.md`. The local surface requires inspection of every displayed source and explicit review, invalidates review after edits, disables insertion after manual fallback, and includes snapshot retrieval timestamps in authorized handovers. Compliance handovers identify Tier-2 compliance; tracing handovers identify Tier-2 payments. These are scripted surface controls, not proof of server-side authorization or live freshness enforcement. The original S1/S2 governance proposals are superseded by this S3 section where they conflict, including raw model-log retention and model-confidence-based matching.

### S3 interface v0.3 — local draft isolation
The demo now keeps text buffers per synthetic ticket in tab memory; no browser storage or backend persistence is used. Revisiting restores only that ticket’s text, with source inspection and approval reset. Manual mode remains paused until explicitly resumed with a fresh review. Existing different editor text requires replacement confirmation; handover previews are invalidated when their inputs change. These are local interaction controls, not live tenant-security evidence. Public hosting remains a static demo of synthetic records.

### Application v0.4 — local workflow and persistence
This extension supersedes the v0.3 “no browser storage” description for the current demo only. Sanitized synthetic case text, outcomes, activity and visible-tab timings are held in per-tab sessionStorage, with schema checks and memory fallback when storage is unavailable. Reset clears the workspace. Known credential/IBAN patterns are redacted; this is not a general anonymization guarantee, and real customer data is excluded. No approval or source inspection is restored. The local journal is editable browser state, not an immutable production audit.

The engine filters public fixtures by assigned merchant, requires a unique reference, checks amount/currency/source schema/freshness/status, and evaluates generated templates before exposure. Its gate is deterministic, not a model score. Compliance/dispute/fund-action requests route to specialists; no legal deadline or diagnosis is generated. The recorded human reply/handovers are local demonstrations, with no external message or financial write. Production authentication, row-level access control, lawful real-data processing, live connectors and model evaluation remain requirements. [P2 coverage](docs/PRODUCT_COVERAGE.md).

## Session 4 — checkpoints and evaluation

9 November 2026. Operations are local and synthetic; no server-side identity or real bank authorization is shipped.

| Checkpoint ⊘ | Kind | Owner and effect |
|---|---|---|
| Sensitive intent, unknown language, missing/ambiguous/stale or inconsistent evidence | Abstention | The engine blocks; the specialist decides on the investigation |
| Payment sources | Approval | The specialist inspects every source, then approves the draft |
| Insertion and editing | Approval | Any edit invalidates the approval; factual check and final approval required |
| Reply / resolution | Approval | The specialist records a local action only; no customer sending |
| Handover | Approval | Reason required, refreshed preview, explicit recording; no real queue contacted |
| Evaluation before a pilot | Exhaustive review | Two independent people, to be named; all 50 labels and outputs reviewed; not mere sampling |

**⏻ Owner and scope:** each specialist can switch their ticket to manual mode in their tab. Assisted insertion is then disabled; resuming resets inspection and approval. The automated scenario "manual fallback and resume require a fresh inspection" passed on 9 November 2026; this is not a test attested by Ops. No global stop exists; Ops must name its owner and test a server-side stop before a pilot.

**Storage and access:** `evals/eval_set_v0.csv`, `fixtures_v0.json`, the JSON results and the CSV grids are versioned in the repository: visible to anyone with access to the repository and potentially to its publication copy. No customer data may enter them. App drafts and notes live in the tab's sessionStorage, with an in-memory fallback; this is neither secure storage nor an immutable journal. Known secret patterns are masked, with no general guarantee of personal-data detection.

**Evaluation integrity:** labels for F21–F50 were AI-proposed before the run; the F01–F20 seed was already exposed. After review and fixes, all 50 became development cases. Do not reuse this set for an independent claim. Human graders must fill in `label_review.csv` and `grader_reviews.csv` themselves; no identity, approval or timing is invented. F19 is fixed: a model score of 0.94 forces abstention; source notes play no part in generation. No real model is evaluated. Code and fixture hashes are in the results. See `evals/report_v0.md`.

## Session 5 — counter-metrics and the segments we report (to come)
*Primary metric (AHT), counter-metrics (QA score, 7-day reopen rate, agent override rate), and protected reporting segments.*

## Session 6 — protected segments and the harm threshold that stops an experiment (to come)
*A/B trial experiment guardrails, enterprise merchant protection, and safety thresholds for experiment termination.*

## Session 7 — accountable owner, rollback authority, incident path (to come)
*Rollback triggers, operational on-call rotation, kill-switch authority, and incident post-mortem playbooks.*
