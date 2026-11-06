"""Generate concise PDF deliverables and refresh the original-format archives."""
from pathlib import Path
from bs4 import BeautifulSoup
support=Path(__file__).with_name('document_support.py').read_text()
support=support.split("(OUT/'README.md').write_text")[0]
support='\n'.join(line for line in support.split('\n') if not line.startswith('export('))
exec(compile(support,'document_support.py','exec'))
CSS+='''
.dense{font-size:9pt;line-height:1.3}.dense h1{font-size:20pt}.dense h2{font-size:11pt;margin:3mm 0 1.5mm}.dense h3{font-size:10pt;margin:2mm 0 1mm}.dense p{margin-bottom:2mm}.dense table{font-size:7.7pt;margin:2mm 0 3mm}.dense td,.dense th{padding:1.5mm}.flow section{break-before:auto}.flow{break-before:page}.flow h1{break-before:auto;font-size:19pt}.flow h2{font-size:11pt}.flow{font-size:9pt;line-height:1.3}.flow table{font-size:7.5pt}.flow td,.flow th{padding:1.4mm}.flow .note{font-size:8pt}.brief th:first-child{width:27%}.brief th:nth-child(2){width:57%}.brief th:nth-child(3){width:16%}.evalcase{break-inside:avoid;border-top:1pt solid #16848a;padding:2mm 0;margin:1mm 0 3mm;font-size:8.1pt;line-height:1.3}.evalcase h2{margin:0 0 1.5mm;font-size:10pt}.evalcase p{margin-bottom:1mm}.identity{font-size:7.8pt;color:#526b77;margin:2mm 0 3mm}
'''
identity='<p class="identity">Team GitHub: @lsantus-mines · @antotototototo18 · Antoine @antorabo75 · @BenjaminAHS · Colin @csib-wq</p>'
def page(title,body):return section(title,body,'dense')

# Four concise pages replace duplicated historical documents and full S3 governance.
p1=intro(1,'Your team, your agent,<br>your problem')+identity+md('''## Team and agent
| Member | GitHub |
|---|---|
| Lenny Santus | @lsantus-mines |
| Anthony Rascle | @antotototototo18 |
| Antoine Rabeau | @antorabo75 |
| Benjamin Caujolle | @BenjaminAHS |
| Colin Sibieude | @csib-wq |

**Company / proposal:** PayFlow B2B, European B2B payments fintech; P2 adapted as FlowAssist. Course scenario: 800 merchants, 12,000 tickets/month, 40% of handling time spent investigating. Other operating figures below are planning assumptions, not verified company observations.

**Job:** When a merchant opens a payment support ticket, FlowAssist retrieves authorised transaction evidence and produces a cited draft in the Zendesk sidebar for a human specialist to review, edit and send.

**Authority:** L1 entity suggestions → L3 tenant-scoped read-only retrieval, human confirms match → L2 drafting/checks → person-only sending; L4 bounded audit metadata. The backend establishes identity; model confidence cannot authorise access.

**Never:** send to a merchant, move/refund/release funds, write the ledger, or disclose a transaction without verified tenant and transaction identity. Ambiguity, stale data or unsupported intent suppress drafting and return to a person.

## Problem in one sentence
Tier-1 payment specialists spend an assumed 7.2 of 18 minutes per ticket investigating disconnected records, equivalent to €414,720/year in investigation labour; today they search manually and draft from memory. Success targets a 30% AHT reduction to 12.6 minutes, QA ≥92% and zero critical data exposures.

## Assumption register
| Figure | Source type / validation |
|---|---|
| 800 merchants; 12,000 tickets/month; 40% investigation | P2 educational scenario, not actual CRM/ticket logs |
| 144,000 tickets/year | Derived: 12,000 × 12 |
| 18-minute AHT; 4.5-hour first response; 18 agents | Guesses; validate with Ops logs and paired timing |
| 7.2 investigation minutes | Derived: 18 × 40% |
| €24/hour; €10/ticket | Planning analogies; wage/cost allocation unverified; do not treat them as identical bases |
| €414,720 investigation value | 144,000 × 7.2 / 60 × €24; capacity estimate |
| 30% saving, QA ≥92%, zero exposure | Product decisions/targets, not measured results |

**Persona:** Karim, Tier-1 specialist, needs to explain a payment without confusing merchant identity, clearing status or bank credit. Ops owns quality, CFO owns investment, DPO/CCO owns data/compliance review. The task is frequent, bounded and reversible before sending.
''')
p2=md('''## Journey and the two pain steps
| Human activity today | Minutes (guess) | Planned assistance |
|---|---:|---|
| Read ticket | 1.5 | L1 entity suggestions |
| Search ledgers / clearing — pain | 5.7 | L3 scoped candidates, person confirms |
| Draft and attach sources — pain | 4.8 | L2 cited draft |
| Check policy / status | 2.5 | Rules block; L2 review |
| Review, edit, send | 2.0 | Person only |
| Categorise and log | 1.5 | L1 route; L4 audit metadata |
| Total | 18.0 | Assumed baseline; not measured |

## Problem tree and five Whys
**Symptom:** merchants wait for payment explanations; specialists switch repeatedly between tools. **Problem:** evidence gathering and reply composition are fragmented.
1. Why slow replies? Specialists investigate before drafting.
2. Why lengthy investigation? Ledger, clearing, dispute and compliance records sit in separate interfaces.
3. Why separate interfaces? Independent services lack a unified support view.
4. Why not one exact lookup? Incoming language often has partial references, dates and gross/net amounts.
5. Why retain a person? Ambiguous identity, status and intent create costly disclosure and financial mistakes.

**Root cause and fix:** fragmented evidence and unstructured requests. First add deterministic read-only joins, source visibility and clear escalation. Use extraction and grounded drafting only where rules/templates are insufficient; improve the workflow and documentation alongside the AI.

## Is AI the right tool?
| Required question | Decision |
|---|---|
| Does a rule solve 80%? | Not established. Benchmark exact references, rules and templates first; the earlier 15% claim is unverified. |
| Prediction/generation or organisation? | Entity extraction and cited wording may need a pretrained model. Permission, money and escalation policy are deterministic/organisational. |
| Do we have the data? | Only synthetic fixtures. Future read-only ledger, clearing and policy access needs owner and DPO approval; no 144k real-ticket corpus supplied. |
| What does an error cost? | S2 judgement: €15 tracing, €90 disputes, €150 compliance; catastrophic disclosure tail remains unpriced. PayFlow owns organisational liability. |

**Chosen level:** bounded GenAI copilot. Rules remain mandatory; classical classification alone cannot compose a cited multi-source explanation. A standalone pretrained model lacks current ledger facts. Autonomous customer action is unjustified; compare hybrid drafting with rules/templates in S4.

## Four selection questions
**Frequency:** course scenario 12,000/month. **Bounded:** read-only account, ledger, clearing and compliance tools; draft, context-only or specialist route. **Measurable:** timing, factual QA, grounding and critical failures per ticket. **Recoverable:** suppress or correct before sending; human review reduces risk but does not guarantee detection.
''')
p3=md('''## Working backwards — fictional launch release
**PARIS — 18 November 2026 (fictional launch exercise).** PayFlow announces FlowAssist for payment support specialists: a verified payment timeline and cited reply inside Zendesk, targeting an AHT reduction from 18 to 12.6 minutes while the specialist retains control. “I can see the evidence before I answer,” says a fictional merchant representative. This quotation and the claimed future improvement are invented solely for the required press-release format, not interview evidence or achieved performance.

## Three hypotheses that must be true
| Hypothesis (guess) | Test and session |
|---|---|
| ≥75% of tracing tickets contain enough evidence for a unique match with ≥99% matching recall | S4: 200 independently labelled cases; compare extraction + deterministic lookup with rules alone; count ambiguous and missed matches. |
| Grounding checker flags unsafe drafts with ≥98% precision | S5: independently grade safe/unsafe draft pairs, including adversarial mismatches; also report unsafe recall and false-safe count. |
| ≥30% overall AHT saving without QA falling below 92% or 7-day reopen exceeding 5% | S6: planned agent-level randomised trial, 9 assisted / 9 control specialists, four weeks; log active review and fallback time. Staffing, thresholds and duration are planning decisions. |

**Economic test connecting S2/S3:** ≥41.2% paired active-time saving on pre-labelled eligible tracing cases; this is different from 30% across the full support mix. A tracing-only pass does not validate dispute/compliance value or production readiness.

## Do nothing over 12 months
| Assumption | Consequence / source type |
|---|---|
| 4% natural efficiency gain through macros and documentation | €57,600/year = 144k × €10 × 4%; planning analogy, not verified trend |
| Merchant/ticket growth +25% | 1,000 merchants and 15,000 tickets/month; scenario guess |
| Four additional hires at €55k loaded cost | €220k/year staffing scenario; do not add again to S2 benefits |
| €35k baseline SLA penalties; +40% absent intervention | €49k/year scenario; contracts and attribution unverified |

The baseline is not zero. S2 compares FlowAssist with this €57,600 efficiency value and the named €125,000/year Merchant Self-Serve Dispute & Reconciliation Portal. Avoid counting growth, hiring avoidance and time savings as independent benefits without evidence.

## P2 adaptation and scope
FlowAssist keeps P2's support investigation job. Initial MVP handles payment tracing; disputes, fraud and compliance route to specialists. No custom-idea pitch is required when using P2; the optional original pitch remains in the source archive.
''')
p4=md('''## Six provisional governance answers
| Question | Specific answer and check owner |
|---|---|
| EU AI Act tier | Internal tracing support; no credit/eligibility decision. Classification and applicable transparency duties require Legal review of actual intended use. Label drafts as AI-assisted. |
| Whose data / legal basis? | Merchant contacts and transaction data, currently synthetic only. DPO must assess purpose, data-subject relationship, contractual necessity or legitimate interests as applicable; no blanket B2B contract approval. |
| Accountability / human | Head of Payment Ops owns answer quality; human specialist reviews/sends; Engineering enforces access and gates. Organisation remains accountable. |
| What must it never do? | No customer sending, ledger/fund writes or unverified tenant/transaction disclosures. Model score never overrides a block. |
| Explainable to whom? | Specialist: facts, IDs, source timestamps and block reasons. Merchant: clear verified status. Authorised auditor: minimised versioned approval/gate metadata. |
| People it cannot serve? | Ambiguous/stale/missing evidence → context-only/manual handling. Dispute, KYC/fraud and unsupported language → named specialist, preserving authorised context. |

## Cost-of-error ownership
Routine rework is priced in S2, but wrong tracing matches can also expose financial data. Dispute misinformation and compliance disclosures create legal/reputational harm beyond operational expected losses. **CCO/DPO** assess data/legal incidents; **Ops** owns quality and specialist routing; **Engineering** owns deterministic authorization and draft shutdown. A second LLM is not a security guarantee.

## Current control requirements
Tenant authorization must precede retrieval. Use parameterised read-only queries, exact transaction checks, redaction, source timestamps and human approval. Wrong-transaction disclosure, tenant exposure or attempted financial/customer action immediately disables drafting; Ops stops, Engineering enforces, DPO/CCO assesses the incident. Live access, provider terms, hosting, no-training/retention and legal classification remain to approve. No compliance certification is claimed.

## Submission and evidence boundary
All numerical operating inputs above are course facts, derived values, decisions, analogies or guesses as marked; no actual PayFlow exports, time study, interviews or signed production terms are available. These statements supersede unsupported historical “measured” claims in the archived source files.

The companion archive preserves README.md, 01_problem_statement.md, governance.md and the optional 00_pitch.md. The assignment requires at least two members to commit with their own accounts; PDF generation cannot supply or certify those contributions. Team alignment with Agentic Workflows must be confirmed by the team; the README currently records “no” for all five members.
''')
a1='<div class="dense">'+p1+'</div>'+page('02 · Diagnosis and AI choice',p2)+page('03 · Hypotheses and baseline',p3)+page('04 · Governance and submission',p4)
export(1,'Assignment_1_Team_Agent_Problem.pdf',a1)

# Keep the one-page CFO memo, and all numerical inputs, but remove duplicate prose.
soup=BeautifulSoup(a2,'html.parser')
memo=str(soup.find('div',class_='compact'))
memo=memo.replace('</h1>','</h1>'+identity,1)
sections=soup.find_all('section',recursive=False)
keep=[]
for sec in sections:
 title=sec.h1.get_text()
 if title.startswith(('01','02','03','04','05','06')):
  if title.startswith('01'):
   # Evidence note and concise caveats, retaining every material model limit.
   sec.clear();sec.append(BeautifulSoup('<h1>Model and assumption register</h1>'+md('''Formula outputs below are recomputed from the original workbook; the editable Excel is retained. All internal-data “measured” claims are educational assumptions, not supplied observations. Base category shares total 100%; Low totals 94% and High 106%, so those scenarios need reconciliation before investment. Retention is €30k judgement; the note's multiplication gives €28,800. Inference/errors are charged to time-equivalents in the original template, not all assisted calls; at 54,654 eligible assisted Base conversations, inference would be about €2,200 rather than €704. Oversight is additional to review time. Keep these historical formulas for transparency, not as an audited forecast.

Rollout remains conditional: Q1 identity/no-send gates; Q2 QA ≥92%, grounding precision ≥98%, zero critical exposures; Q3 ≥41.2% paired saving plus independent review; Q4 continued guardrails. Integration is amortised, so annual net value is not year-1 cash flow. Do not double-count staffing avoidance.
'''),'html.parser'))
  keep.append(str(sec))
annex=''.join(keep)
annex=annex.replace('<section','<section')
# Remove forced per-register breaks; keep larger chapter starts only.
annex_soup=BeautifulSoup(annex,'html.parser')
for h in annex_soup.find_all('h1'):
 if h.get_text().startswith('04'):
  h.name='h2';h.string=h.get_text().replace('04 · Assumption register — ','Inputs — ')
# Build/buy summary is concise and carries the break-even omitted from the large legacy prose.

for t in annex_soup.find_all('table'):
 if len(t.find_all('th'))==6:
  for th,width in zip(t.find_all('th'),[27,7,7,7,14,38]):th['style']=f'width:{width}%'
annex=str(annex_soup)+md('''### Build/buy interpretation and cost-of-error ownership
Weighted scores: Build 3.15, Buy 2.15, Orchestrate 4.35; weights sum to 100%. These are judgements, not vendor diligence. Internal comparable cost = €49,500 + €0.04025 × N; vendor scenario = €0.92 × N. Break-even ≈56,266 time-equivalent resolutions/year. At 17,489.16 equivalents, internal €50,204 vs vendor €16,090; buying is €34,114 cheaper on this limited comparison. Connector/platform fees, commercial terms and real billable outcomes must be checked; a copilot time-equivalent is not automatically a billable outcome.

CCO/DPO own disclosure and regulatory risk; Ops owns wrong answers/deadlines and oversight; Engineering owns authorization, exact checks and shutdown. €15/€90/€150 error severities price operational loss, not the catastrophic tail. Model confidence cannot authorize a match; any critical exposure disables drafts. Reporting duties require incident assessment.

Sources/Assignment_2_sources.zip retains the editable workbook, original memo and governance. Two genuine member-authored commits remain required. The PDF's one-page memo and recalculated annex supersede historical overclaims; original source limitations are explicitly disclosed.
''')
export(2,'Assignment_2_Sizing_Investment_Memo.pdf',memo+'<div class="flow">'+annex+'</div>')

# S3 keeps single-page v2, canvas, v1; concise annexes contain all required details.
a3=onepage('03_product_brief.md','Product brief · v2').replace('</h1>','</h1>'+identity,1)
a3+=onepage('03_ai_lean_canvas.md','AI Lean Canvas · v2')
a3+=onepage('research/brief_v1.md','Product brief · archived v1')
design=read('03_design_details.md')
design=design.split('## 1.')[1].split('## 6.')[0]
# Drop duplicated introductory paragraph, keep full process/RICE/model tables.
design='## 2.'+design.split('## 2.',1)[1]
a3+='<div class="flow">'+section('Process, features and component model',md(design))
research=re.sub(r'^# .*\n','',read('03_user_research.md'),flags=re.M)
a3+=section('Design loop, prototype and acceptance tasks',md(research)+md('''## Prototype and original prompt
**Public link:** https://deploy-project-product-management.vercel.app. Last source-recorded HTTP verification: 3 November; no new availability or rendering claim. Local `prototype/index.html` needs no installation or API key. Runtime is deterministic with synthetic fixtures, not connected to Zendesk, banks or a model.

**Tool / time box:** Codex-assisted HTML/CSS/JS. Initial build duration was not instrumented; under-one-hour compliance is unproven. Later versions add local workflow features, not completed participant tests.
''')+md(read('03_prototype_link.md').split('## The prompt used')[1].split('## Test walkthrough')[0]))
a3+=section('Spec skeleton and measurement plan',md('''## User, trigger and scope
Karim receives an assigned merchant ticket. Confirm identity and intent; retrieve authorised read-only ledger/clearing evidence; confirm a unique transaction; draft only eligible tracing; inspect all sources; human reviews/edits/sends. Always allow manual handling or safe specialist handover. Disputes, KYC/AML, refunds and autonomous sending remain out of scope.

## Input / output contract
Input: ticket ID/text/language, authenticated merchant and assigned specialist, source IDs/timestamps, transaction reference, amount in integer minor units, currency and policy version. Extracted entities are untrusted hints; no model SQL. Output: `draft_ready | context_only | human_only`, cited draft or null, authorised evidence, block reason and specialist route. No customer-send or financial-write tool exists.

## Deterministic gates and state
Verify assigned-agent access and tenant before retrieval. Unique reference, currency, amount/gross-net reconciliation and source identity must agree; amount alone never authorises. Missing/stale/contradictory evidence, malformed output, timeout or sensitive intent suppresses drafts. Provisional freshness ≤5 min, retrieval ≤2s and total pipeline ≤10s require validation. A model score cannot override rules.

`loading → draft_ready | context_only | human_only`. Insertion requires all sources inspected and explicit approval. Edits invalidate approval; ticket changes reset inspection/review. Manual mode disables insertion; resuming requires fresh review. Handover preserves authorised IDs, timestamps, reason and notes; compliance goes to Tier-2 compliance, tracing to Tier-2 payments. Session restoration never restores approvals. Local receipts and audit are editable browser state, not authenticated production records.

## Edge cases and fallback
No/multiple match → request unique reference; foreign/forged tenant → empty context and block; unexplained currency/gross-net mismatch → context only; stale/conflicting feed or timeout → suppress; unsupported language, dispute, fraud or KYC → person; injection cannot change scope; credentials/IBAN are redacted, failed redaction routes manually. Never turn “sent to bank” into “beneficiary credited” or invent an ETA, deadline, refund or hold-release advice.

## Done criterion and denominator
Use the one-sentence success criterion in brief v2: frozen 200 synthetic tracing cases, eligibility labelled before execution, ≥41.2% total active-time saving including review and fallback; QA ≥92%, unsafe-draft flag precision ≥98%, zero critical exposures. Saving = `1 − sum(assisted active time) / sum(manual active time)` over all pre-labelled eligible cases; failures stay in the denominator. Randomise/counterbalance paired timing; report raw intervals, agent count and uncertainty. Do not replace measured manual time by the 18-minute assumption.

Two independent graders check tenant/transaction, money/status/time, citations, safe action and wording. QA rubric: factual accuracy 40, source coverage 25, policy safety 25, clarity 10; critical failure overrides score. Grounding precision = unsafe flags confirmed unsafe / all unsafe flags; also report recall and false-safe count. No flags means undefined precision. Disagreement remains fail/pending adjudication.

## Seed origin and freeze
The 20 inputs and initial labels are AI-generated and not human-approved. Two real reviewers must independently check every label/reference and reconcile before freezing a commit and policy version. Keep development/demo cases separate from held-out evaluation, deduplicate by scenario family. Expand to 50 for A4, then 200 tracing cases. The seed does not prove performance or represent the production mix. Seven cases are proposed timing-eligible; thirteen exercise blocking/handover.
'''))
# Retain full audit and retention/trust tables without repeating old sessions or implementation changelog.
gov_short='## Six-question'+g3.split('### Six-question',1)[1]
gov_short=gov_short.split('### S3 v2 design decisions')[0]
a3+=section('Data audit and governance',md(gov_short))
a3+=section('Evaluation policy and all 20 cases',md(re.sub(r'^# .*\n','',read('evals/reference_policy.md'),flags=re.M))+md('''## Input-generation recipe and review status
Generate fictional merchant tickets plus self-contained ledger/clearing snapshots under FLOW-POL-1. Cover easy/hard/adversarial/out-of-scope cases; EN/FR/DE and unsupported PT, EUR/SEPA and USD/SWIFT, SMB/Enterprise. Never import actual customer records. Original CSV, generation notes, policy and blank human-review register are in the source archive. The records below preserve every original field, including origin; labels are proposed, not human-approved.
'''))
for row in csv.DictReader((REPO/'evals/eval_set_v0.csv').open()):
 values=list(row.items());ident=next(iter(row.values()))
 a3+='<article class="evalcase"><h2>'+html.escape(ident)+' · '+html.escape(row.get('segment',''))+'</h2>'
 for k,v in values:
  if k=='id':continue
  a3+='<p><b>'+html.escape(k.replace('_',' '))+':</b> '+html.escape(v)+'</p>'
 a3+='</article>'
a3+=section('Submission checklist and unresolved requirements',md('''**Deadline:** 8 November 2026 per supplied DOCX; PDF edition 6 November. Same P2 team/agent and S2 flip point. The one-page v2, canvas and archived v1 precede process, RICE, model, data audit, research record, prototype prompt, spec and 20 complete cases.

**Unfulfilled human requirements:** three real 20-minute past-behaviour conversations; two users attempting a task aloud; evidence-based changes to v2; manual labelling; and every member's own authored commit. No interview, approval or contribution is invented. Current D01–D05 are desk decisions; T01/T02 are acceptance tasks, not completed participant usability tests. Under-one-hour initial prototype construction is not demonstrated.

Users may inform workflow and wording, but CFO/Product owns the 41.2% hurdle, independent timing/graders establish performance, Engineering evaluates model choices, DPO/Legal approves processing/retention and CCO/Ops approves scope. A tracing-only success does not validate S2's dispute/compliance or strategic value.

**Original formats:** Sources/Assignment_3_sources.zip retains all required Markdown, original v1, CSV, policy, blank human review register and clickable prototype. The PDF condenses their presentation; it does not replace the repository or establish full assignment compliance. Live identity, bank/Zendesk access, model-based evaluation, causal time savings and production readiness are not demonstrated.
'''))+'</div>'
export(3,'Assignment_3_MVP_Brief_and_Design_Loop.pdf',a3)
(OUT/'Sources'/'validation.json').write_text(json.dumps(checks,indent=2))
(OUT/'README.md').write_text('''# Assignments — FlowAssist · version synthétique

PDF révisés le 6 novembre 2026. Antoine : **@antorabo75** ; Colin : **@csib-wq**. Identifiants corrigés dans le README du projet, les PDF, les HTML et les archives sources.

- Assignment 1 : synthèse du problème, diagnostic, hypothèses, baseline et six réponses de gouvernance.
- Assignment 2 : mémo d’une page, modèle, registre complet Low/Base/High, sept coûts, sensibilité, build/buy, prix et risques.
- Assignment 3 : brief v2, Lean Canvas et brief v1 d’une page chacun ; annexes condensées avec processus, RICE, audit, recherche, prompt, spec et les 20 cas complets.

Les consignes nécessitant des actions humaines restent explicitement non attestées : entretiens, essais utilisateurs, labels humains et contributions Git personnelles. Les limites du modèle financier original restent signalées. Les PDF ne prétendent pas à une conformité totale quand les preuves manquent.

Les archives Sources conservent les fichiers requis dans leur format d’origine et les consignes DOCX. Les hypothèses et anciennes affirmations de sources non vérifiées y sont conservées pour traçabilité ; les corrections explicites des PDF prévalent. Génération : depuis la racine du dépôt project-product-management, `/opt/anaconda3/bin/python Assignments/Sources/build_assignments.py`.
''')
