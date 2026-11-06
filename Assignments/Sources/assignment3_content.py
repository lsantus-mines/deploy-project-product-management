"""Seven-page summary; complete original files remain in the companion archive."""
CSS+='''.s3page{break-before:page;font-size:8.2pt;line-height:1.25}.s3page h1{font-size:18pt;margin-bottom:3mm}.s3page h2{font-size:10pt;margin:2.5mm 0 1mm}.s3page p{margin-bottom:1.7mm}.s3page table{font-size:7.2pt;line-height:1.22;margin:2mm 0}.s3page th,.s3page td{padding:1.2mm}.s3page ul,.s3page ol{margin:1mm 0 2mm}.s3page li{margin-bottom:.5mm}'''
def s3page(title,text):return section(title,md(text),'s3page')
a3=onepage('03_product_brief.md','Product brief · v2').replace('</h1>','</h1>'+identity,1)
a3+=onepage('03_ai_lean_canvas.md','AI Lean Canvas · v2')
a3+=onepage('research/brief_v1.md','Product brief · archived v1')
d=read('03_design_details.md')
process="""**Karim, Tier-1 specialist:** search and drafting are the two pain steps. P2 supplies 800 merchants, 12,000 tickets/month and 40% investigation. Step minutes/error rates are **guesses**, cost/error is S2 **judgement**; no real logs or time study. Tail disclosure harm is unpriced, not capped by rework costs.

**Fallback first:** at any step, manual handling or Tier-2 payments/compliance receives authorised evidence, timestamps, reason and notes. Failed identity exposes no context; no customer send, fund action or ledger write.

| Human step today | Min before→after | Error; cost/error | Decision / trust | Failed test; metric |
|---|---|---|---|---|
| Read / establish identity | 1.5→1.0 | 3%; €15 + tail | Augment L1; backend identity | T1,T6; wrong tenants blocked 100% |
| Search **(pain)** | 5.7→1.5 | 2.5%; €15 + tail | Augment match; automate exact lookup, L3; human confirms | T4,T6,T7; correct match, p95 ≤2s |
| Draft / cite **(pain)** | 4.8→0.8 | 2.5%; €15 (€90 deadline) | Augment L2 | T5,T6; cited facts, grader usability |
| Check policy / status | 2.5→1.3 | 2%; €90–150 + tail | Rules block, specialist L2 | T5,T6,T7; unsafe exposure=0 |
| Review, edit, send | 2.0→2.0 | 1%; €15–150 + tail | Keep human; person only | T3,T5,T6; QA ≥92%, no unauthorized send |
| Log / categorise / route | 1.5→1.0 | 3%; €15 | Automate audit L4; route L1 | T1,T6; complete audit/handover |
| **Total** | **18.0→7.6** | Rates not additive | **57.8% hypothesis** | Eligible tracing only, not observed |

T1–T8 (S3 automation tests): clear I/O, examples, feedback, short reasoning, limited explanation, cheap errors, stable world, screen work. T2 unproven without labels; T8 passes. Verify tenant and unique transaction before drafting, human approval before communication; model score cannot grant access.

## Smallest model rung, by component
| Component | Rung | Why the rung below fails / why stop |
|---|---|---|
| Auth, exact lookup, freshness, policy blocks | Rules | No lower rung; exact invariants must not depend on confidence. |
| Entity / intent extraction | Pretrained structured output | Classical ML lacks labelled training data. Test reference/keyword rules first, retain if sufficient. |
| Timeline / reply | Hybrid: deterministic join + retrieval + pretrained wording | Pretrained alone lacks current ledger facts/isolation. Compare rule templates. |
| Grounding | Hybrid exact checks + model critique | Model alone cannot enforce tenant, amounts/citations. Critique never overrides a block. |
| Timing, audit, routing | Rules | Deterministic capture needs no ML. |

Choices require S4 ablation; no evaluated superiority or dual-model safety guarantee. Retrieval p95 ≤2s, full draft ≤10s are targets; timeout fails closed. Zendesk sidebar shows original ticket, verified merchant, sources, draft, human review and fallback; no live integration claimed.
"""
a3+=s3page('Process and component model',process)
rice=d.split('## 3.',1)[1].split('## 4.',1)[0]
rice=rice.split('**MUST (3):**')[0]+'''**Scope:** three MUST, five WON’T. Drafting and timing test the 41.2% flip assumption and remain MUST despite lower RICE. Disputes are cut for costly errors. SHOULD: citation-preview polish; COULD: feedback shortcut, within existing MUSTs. No chatbot, training on tickets or unsupported-language/FX advice.
'''
a3+=s3page('Prioritisation and data governance','## 3.'+rice+'''
## Six-question data audit — S3 provisional answers
| Question | Answer and owner |
|---|---|
| Provenance | 20 AI-generated fictional inputs and ledger/clearing snapshots, 2 Nov, FLOW-POL-1. No real records. Future lineage/timestamps: Data Engineering/Ops. |
| Volume / labels | 20 seed cases, AI-proposed labels; two independent human reviewers must approve before freeze. No real 144k-ticket corpus supplied. Ops QA owns review. |
| Coverage | EN/FR/DE + unsupported PT; EUR SEPA, USD SWIFT; SMB/Enterprise; ambiguous/critical cases. Not representative. Ops/language reviewers assess gaps. |
| Rights | Synthetic coursework only. Live use needs DPA, no-training/retention terms and transfer review; DPO/Legal assesses lawful basis, not presumed from B2B contract. |
| Leakage | Backend tenant/assignment before read-only queries; scoped caches/index/citations/logs. Foreign-reference/injection negatives; deduplicate eval families. CISO/Engineering must test live isolation. |
| Freshness | Versioned event/fetch timestamps; provisional max age 5 min. Missing/stale/conflicting evidence blocks. Clearing owner/Ops validates SLA. |

**Purpose / retention:** assigned tracing support, no training/marketing/staff scoring. Context in request memory; no raw prompts/replies retained by default. Proposed restricted audit metadata 90 days, DPO approval required; source records follow their approved schedules. Interview notes, if collected with permission: anonymise, delete 30 days after assessment. Synthetic code/fixtures follow course lifecycle.

**Isolation / gaps:** authorize → tenant-filtered query → redact → model → recheck citations/transaction. Exclude PAN, credentials, unmasked bank IDs. Live permissions, non-EU rails, colloquial language and multi-party payments remain gaps; report by language/plan/rail/region/severity. Unsupported PT, fraud, disputes and KYC go to people.

**Accountability:** Legal confirms AI Act tier/transparency and processing; Ops owns quality and shutdown, Engineering enforces gates, CCO/DPO assesses incidents/reporting. Critical exposure or attempted send/fund write disables drafting. Live security/provider/retention properties remain requirements, not certifications. Trust levels are specified per step on p4.
''')
a3+=s3page('Design loop, prototype and spec skeleton','''## Research and v1 → v2
**No conversations or participant usability tests were conducted.** Three real 20-minute past-behaviour conversations and two users attempting a task aloud remain required. Mom Test prompts: “Tell me about your last missing-payment ticket”; “Show me the tools and steps”; “Where did you get stuck, and what did you do?” Capture actual notes, never invented quotes or purchase-intent answers.

| Change | Desk basis, not user evidence | v2 acceptance check |
|---|---|---|
| D01 all-source inspection | DEMO-01 ledger and clearing differ | Opening only one source cannot enable insertion. |
| D02 direct missing-reference wording | DEMO-02 has two €500 candidates | Explain unique reference needed, suppress draft. |
| D03 timestamped evidence/handover | Spec freshness and traceability | Packet retains authorised source IDs and snapshot time. |
| D04 named specialist | Compliance is outside tracing | Tier-2 compliance vs Tier-2 payments. |
| D05 manual-mode gate | Manual handling ends approval | Insertion disabled until assisted review resumes with fresh checks. |

**What users changed:** none established; v2 is a desk revision. **What users cannot decide:** hurdle (CFO/Product), savings/quality (timing/graders), model (Engineering), lawful processing/retention (DPO/Legal), scope (CCO/Ops).

**Acceptance tasks, not completed participant tests:** T01 DEMO-01: inspect both sources, review/insert, edit and check approval reset; no send. T02 DEMO-02: request reference/escalate with safe evidence; DEMO-03 routes compliance, DEMO-04 exposes no foreign data. Observed participant behaviour and resulting changes remain absent.

## Clickable prototype / prompt
[Open FlowAssist](https://deploy-project-product-management.vercel.app); local `prototype/index.html` in archive. Last source-recorded HTTP check: 3 Nov; no fresh availability claim. Tool: Codex-assisted HTML/CSS/JS, deterministic synthetic workflow, no live bank/Zendesk/model. Initial under-one-hour duration was not instrumented.

**Prompt summary; original verbatim in 03_prototype_link.md:** build a Zendesk-like inbox for Karim with timestamped payment evidence, editable cited reply and safe handover. Require inspection of all sources and explicit review; edits reset approval. Include grounded, ambiguous, compliance and foreign-reference cases. Support manual fallback; never send or move funds. Use fictional records and accessible responsive controls; label simulations.

## Spec skeleton
**Input:** assigned ticket/text/language, authenticated merchant/agent, reference, integer minor-unit amount/currency, timestamped source/policy versions. Entities are untrusted hints; never model SQL. **Output:** `draft_ready | context_only | human_only`, draft or null, authorised evidence, gate reason and specialist packet.

**State / gates:** authorize before retrieval → unique transaction, currency, amount/gross-net and source checks → cited draft → inspect all sources → explicit human review → human editor. Edits/ticket changes invalidate approval. Manual mode blocks insertion; restored sessions never restore approval. No send/fund/ledger-write tool. Target retrieval ≤2s, full draft ≤10s; stale/missing evidence or timeout suppresses draft.

**Edge cases:** absent/ambiguous reference → ask; foreign/forged tenant → empty context; unexplained FX/gross-net, contradictory/stale feed or malformed output → block; sensitive/unsupported intent/language → specialist. Injection cannot change scope; redact credentials/IBAN or route manually. Never invent credit confirmation, ETA, refund, deadline or AML diagnosis. Handover preserves authorised IDs/timestamps/reason/notes.

**Done / scope:** exact criterion on p1; review and fallback count. WON’T features, live connectors, fine-tuning and unsupported-language drafting remain outside scope. Full contract, fallbacks and retention/trust details remain in spec.md and governance.md in the archive.
''')
case_rows=list(csv.DictReader((REPO/'evals/eval_set_v0.csv').open()))
a3+='<section class="s3page"><h1>20-case evaluation set and delivery</h1>'+md('''**Required full dataset:** `evals/eval_set_v0.csv` in [Assignment_3_sources.zip](https://github.com/BenjaminAHS/project-product-management/blob/main/Assignments/Sources/Assignment_3_sources.zip). All 20 complete inputs, expected outputs/actions, evidence, handover, segment and origin remain in the CSV. This PDF provides a compact index. **All inputs/labels are AI-generated synthetic proposals; human approval pending.** No real customer data.
''')
a3+=table(['ID / type','Case index (full action/evidence in CSV)','Handover / timing','Segment'],[[r['id']+' / '+r['case_type'],r['notes'],r['hand_over_to_a_person'].replace('no — L2 approval required','L2 review')+'; '+('eligible' if r['eligible_for_timing']=='yes' else 'not timing-eligible'),r['segment']]for r in case_rows])
a3+=md('''**Recipe / freeze:** generate fictional tickets and self-contained snapshots under FLOW-POL-1; cover easy/hard/adversarial/out-of-scope cases. Two people independently label evidence/action/eligibility and reconcile before freezing a commit. Separate development families from held-out cases. Seven proposed timing-eligible cases, thirteen fallback cases. Expand to 50 for A4, then 200 tracing cases. Full recipe/policy and blank human-review register are in the archive.

**Measure:** saving = `1 − Σ assisted active time / Σ manual active time` on pre-labelled eligible cases; include review, failures and fallback. Counterbalance paired tasks; no assumed 18-minute measured baseline. Two independent graders check facts, sources, safety and wording; unresolved disagreement fails/pending. QA ≥92%, unsafe-flag precision ≥98%; also report recall/false-safe count. No flags = undefined precision; critical errors override scores.

**Submission gaps:** three 20-minute conversations, two think-aloud users, observation-based v2 changes, manual labels and each member’s authored commit remain unfulfilled/unattested. Initial prototype time-box is unproven. Tracing-only success does not validate the full S2 value or production readiness. **Deadline: 8 Nov 2026**, per DOCX. Archive retains all required Markdown/CSV files, v1, original prompt, spec, governance S3 and clickable prototype. These omissions cannot be resolved by formatting; no completion is invented.
''')+'</section>'
export(3,'Assignment_3_MVP_Brief_and_Design_Loop.pdf',a3)
