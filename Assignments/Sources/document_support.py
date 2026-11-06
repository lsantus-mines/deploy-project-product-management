from pathlib import Path
import re,html,csv,json,zipfile,sys
import cffi
orig=cffi.FFI.dlopen
lib=Path('/Applications/Inkscape.app/Contents/Resources/lib')
libs={'libpango-1.0-0':'libpango-1.0.0.dylib','libgobject-2.0-0':'libgobject-2.0.0.dylib','libharfbuzz-0':'libharfbuzz.0.dylib','libharfbuzz-subset-0':'libharfbuzz-subset.0.dylib','libfontconfig-1':'libfontconfig.1.dylib','libpangoft2-1.0-0':'libpangoft2-1.0.0.dylib'}
cffi.FFI.dlopen=lambda self,name,*a,**k:orig(self,str(lib/libs[name]) if name in libs else name,*a,**k)
from weasyprint import HTML
import markdown
sys.path.insert(0,'/opt/homebrew/lib/python3.14/site-packages')
import openpyxl
REPO=Path(__file__).resolve().parents[2]; ROOT=REPO.parent; OUT=REPO/'Assignments'
TEAM='Lenny Santus · Anthony Rascle · Antoine Rabeau · Benjamin Caujolle · Colin Sibieude'
CSS='''
@font-face{font-family:Body;src:url("file:///System/Library/Fonts/Supplemental/Arial.ttf")}
@font-face{font-family:Body;src:url("file:///System/Library/Fonts/Supplemental/Arial Bold.ttf");font-weight:700}
@page{size:A4;margin:17mm 16mm 17mm;@top-left{content:"FLOWASSIST / PAYFLOW B2B";font:8pt Body;color:#557079}@top-right{content:string(assignment);font:8pt Body;color:#557079}@bottom-left{content:"MSA-DAT07-04 · Team project · 6 November 2026";font:7.5pt Body;color:#657480}@bottom-right{content:counter(page);font:8pt Body;color:#657480}}
*{box-sizing:border-box}body{font:10pt/1.4 Body, sans-serif;color:#233344}h1{font-size:24pt;line-height:1.12;color:#123646;margin:0 0 5mm}h2{font-size:14pt;line-height:1.2;color:#146e76;margin:6mm 0 2.5mm;break-after:avoid}h3{font-size:11pt;color:#123646;margin:4mm 0 2mm;break-after:avoid}p{margin:0 0 2.8mm}ul,ol{padding-left:5mm;margin:2mm 0 3mm}li{margin-bottom:1mm}table{border-collapse:collapse;width:100%;font-size:8.1pt;line-height:1.3;margin:3mm 0 4mm;table-layout:fixed}thead{display:table-header-group}th{background:#153e4c;color:white;font-weight:700}th,td{padding:2mm 2.1mm;border-bottom:.5pt solid #d9e3e7;text-align:left;vertical-align:top;overflow-wrap:anywhere}tbody tr:nth-child(even){background:#f0f5f6}tr{break-inside:avoid}a{color:#08747c;text-decoration:none;overflow-wrap:anywhere}blockquote{margin:3mm 0;padding:3mm 4mm;background:#edf5f5;border-left:3pt solid #16848a}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f4f6;padding:3mm;font-size:7.4pt}code{font-size:.9em;overflow-wrap:anywhere}section{break-before:page}.kicker{font-size:9pt;font-weight:700;letter-spacing:1.5pt;color:#13828a;margin-bottom:4mm;string-set:assignment content()}.meta{font-size:8pt;color:#657480;margin-bottom:5mm}.note{padding:3mm 4mm;background:#fff5e5;border-left:3pt solid #d5a147;font-size:9pt;margin:4mm 0}.compact{font-size:8.6pt;line-height:1.28}.compact h1{font-size:19pt}.compact h2{font-size:10pt;margin:2.7mm 0 1.3mm}.compact p{margin-bottom:1.8mm}.compact table{font-size:7.4pt;margin:1.8mm 0}.compact td,.compact th{padding:1.5mm}.compact ul,.compact ol{margin:1mm 0 2mm}.compact li{margin-bottom:.4mm}.wide table{font-size:7.2pt}.wide td,.wide th{padding:1.5mm}.case{break-before:page}.case h2{font-size:17pt}.case dt{font-weight:bold;color:#146e76;margin-top:4mm}.case dd{margin:1mm 0 2mm;font-size:9.2pt;overflow-wrap:anywhere}.small{font-size:8pt;color:#657480}.brief{font-size:8pt;line-height:1.22}.brief h1{font-size:18pt}.brief h2{font-size:9pt;margin:2.1mm 0 1mm}.brief p{margin-bottom:1.4mm}.brief blockquote{padding:2mm 3mm;margin:2mm 0}.brief .kicker{margin-bottom:2mm}.hero{font-size:12pt;color:#146e76}.toc li{margin:3mm 0}
'''
def md(s):
 s=re.sub(r'\[([^\]]+)\]\((?!https?://|#)([^)]+)\)',lambda m:'['+m[1]+'](https://github.com/BenjaminAHS/project-product-management/blob/main/'+m[2].replace('../','')+')',s)
 return markdown.markdown(s,extensions=['tables','fenced_code','sane_lists'])
def read(n):return (REPO/n).read_text()
def section(title,body,cls=''):
 return f'<section class="{cls}"><h1>{html.escape(title)}</h1>'+body+'</section>'
def intro(n,title):return f'<div class="kicker">ASSIGNMENT {n}</div><h1>{title}</h1><p class="hero">FlowAssist — Agent-assist copilot for B2B payments</p><p class="meta">Data & AI Product: From Diagnosis to Delivery · Albert School / Mines Paris-PSL<br>{TEAM}<br>PDF edition · 6 November 2026 · Coursework in English, following the supplied briefs.</p>'
def table(head,rows):return '<table><thead><tr>'+''.join('<th>'+html.escape(str(v))+'</th>'for v in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(v if v is not None else ''))+'</td>'for v in row)+'</tr>'for row in rows)+'</tbody></table>'
checks={}
def export(n,name,content):
 doc=HTML(string='<html lang="en"><head><meta charset="utf-8"><title>Assignment '+str(n)+' — FlowAssist</title><style>'+CSS+'</style></head><body>'+content+'</body></html>',base_url=str(REPO)).render()
 doc.write_pdf(OUT/name)
 checks[str(n)]={'file':name,'pages':len(doc.pages),'headings':[],'overflow':[]}
 for i,p in enumerate(doc.pages,1):
  for b in p._page_box.descendants():
   if b.element_tag in ['h1','h2'] and b.__class__.__name__=='BlockBox':
    t=''.join(x.text for x in b.descendants() if hasattr(x,'text'))
    checks[str(n)]['headings'].append([i,t])
   if getattr(b,'text',None) and b.position_y < p.height-60 and (b.position_x+b.width>p.width-42 or b.position_y+b.height>p.height-46):
    checks[str(n)]['overflow'].append([i,b.text[:70],round(b.position_x),round(b.position_y),round(b.width)])
 print(name,len(doc.pages),'pages')
 (OUT/'Sources'/('Assignment_'+str(n)+'.html')).write_text('<html><head><meta charset="utf-8"><style>'+CSS+'</style></head><body>'+content+'</body></html>')

# Historical source material is accompanied by the corrections already made in S3.
gov=read('governance.md'); g1=gov.split('## Session 1')[1].split('## Session 2')[0];g2=gov.split('## Session 2')[1].split('## Session 3')[0];g3=gov.split('## Session 3')[1].split('## Session 4')[0]
evidence='''<div class="note"><b>Evidence status.</b> PayFlow is an educational scenario. The P2 proposal supplies 800 merchants, 12,000 tickets/month and 40% investigation time. The repository contains no real company logs, time study, interviews, contracts or approved production deployment. Earlier internal “measured” statements are scenario assumptions; they do not attest to observations. All other operating figures are assumptions or analogies to validate. Product outcomes and the launch quotation are fictional targets. The current S3 governance supersedes earlier proposals where they conflict.</div>'''
a1='<div class="compact">'+intro(1,'Your team, your agent,<br>your problem')+evidence
readme=read('README.md').split('## Team')[1].split('## Repository structure')[0]
a1+=md('## Team'+readme)
a1+=md('''## Submission scope
This PDF consolidates the README, problem statement, optional P2-adaptation pitch and provisional governance. The assignment requires the repository files and commits from at least two members using their own accounts. The companion source archive preserves these files; PDF packaging does not establish individual authorship.
''')
prob=read('01_problem_statement.md')
prob=prob.replace('**Measured**','**Scenario assumption**').replace('| Measured |','| Scenario assumption |')
prob=prob.replace('Active enterprise and marketplace merchant accounts in CRM (Q3 2026).','P2 course proposal; no CRM export supplied.').replace('Zendesk ticket logs averaged over the trailing 12 months (144,000 tickets/yr).','P2 course proposal: 12,000/month; 144,000/year derived, no logs supplied.').replace('Time-and-motion study on 250 sampled tickets tracked via screen-recording in June 2026.','P2 course proposal: 40%; no time-and-motion study supplied.').replace('Median handling time recorded across tier-1 Zendesk payment queues.','Assumed 18-minute AHT, to be measured; no handling-time extract supplied.').replace('Zendesk SLA monitoring metrics over Q1–Q3 2026.','Assumed first-response time; no SLA monitoring extract supplied.').replace('Existing internal Support QA rubric (accuracy, tone, compliance citation, policy adherence).','Proposed quality target; no internal QA rubric supplied.').replace('Guess (supported by exploratory 50-ticket audit)','Guess (exploratory audit not supplied)').replace('**Yes, 100 % owned internally within PayFlow\'s VPC.**','**Proposed future data, not supplied in this repository.**').replace('**FlowAssist L4 Retrieval lands here**','**Tenant-scoped L3 retrieval is proposed here**').replace('**FlowAssist L4 Grounding Evaluator checks here**','**Rules plus L2 specialist checks are proposed here**').replace('**Human L1 accountability**','**Person-only approval and sending**')
prob=prob.replace('## 5. Press release (Working Backwards)','## 5. Press release (Working Backwards)\n\n**Fictional future launch exercise. The quotation and outcomes below are invented for the required press-release format, not user research or measured performance.**')
# Mark all historical quantitative statements and unsupported analogies explicitly.
prob=prob.replace('## 7. Do-nothing baseline','## 7. Do-nothing baseline\n\n**Source type:** 4% annual efficiency gain is a planning analogy from S2 (unverified); growth, hiring, penalties, turnover and timing are scenario guesses, not measured company results. Validate with Ops staffing, SLA and turnover records. The €220k hiring scenario is not added again to S2 benefits.')
a1+='</div>'
a1+=section('01 · Problem and working backwards',md(prob))
a1+=section('02 · Governance — provisional answers',evidence+md('## Session 1'+g1+'\n## Session 2'+g2))
a1+=section('03 · Current governance corrections',md('## Session 3'+g3))
a1+=section('04 · Supporting pitch',evidence+md(read('00_pitch.md')))
a1+=section('05 · Assignment 1 compliance map',table(['Supplied requirement','Evidence in this package'],[
 ['Team, company, trigger → action → outcome, trust, never rule','Opening team/agent section; current trust table'],['Quantified problem with sources','Problem §1; evidence correction note supersedes historical “measured” claims'],['Problem tree, 5 Whys and type of fix','Problem §2'],['Four AI questions and level below','Problem §3'],['Frequency, bounded space, measurable success, recoverability','Problem §4; human checking reduces but does not eliminate error'],['Launch release and three hypotheses with sessions','Problem §§5–6; fictional release explicitly labelled'],['Non-zero 12-month do-nothing','Problem §7 and S2 quantified comparison'],['Six governance questions and pending checks','Governance S1 plus current S3 corrections'],['At least two members commit with own accounts','Requires actual Git history; not certified by this PDF']]))
export(1,'Assignment_1_Team_Agent_Problem.pdf',a1)

# Sizing: calculate directly from workbook inputs (formula caches are empty).
w=openpyxl.load_workbook(REPO/'02_sizing.xlsx',data_only=False); s=w['Inputs'];results=[]
for c in [3,4,5]:
 v=lambda r:s.cell(r,c).value
 adopt=sum(v(r)for r in range(39,43))/4
 eq=[v(6)*12*v(14+i)*v(18+i)*v(22+i)*v(34+i)*adopt for i in range(3)]
 gross=[x*v(9)for x in eq];err=[eq[i]*v(26+i)*v(30+i)for i in range(3)];ai=[x*v(45)*v(46)for x in eq]
 fixed=[v(49)/v(50),v(51),v(52)*v(53),v(54),v(55)*v(56)]
 net=sum(gross)-sum(err)-sum(ai)-sum(fixed)+v(67)+v(68)
 results.append(dict(adopt=adopt,eq=eq,gross=gross,err=err,ai=ai,fixed=fixed,net=net,other=v(67)+v(68),dn=v(59)*v(6)*12*v(9),hurdle=v(60)))
base=results[1];ev=sum(results[i]['net']*s.cell(63,3+i).value for i in range(3))
money=lambda x:'€'+format(x,',.0f')
a2='<div class="compact">'+intro(2,'Investment memo')+md(f'''**CONDITIONAL GO** if paired active handling-time saving is **≥41.2%** on pre-labelled eligible tracing cases, grounding-check precision **≥98%**, QA **≥92%** and critical exposures **zero**; independently validate before any production investment.

### How much?
Year-1 base net value is **{money(base['net'])}**, on 144,000 annual tickets at €10/ticket. The three-category S2 model yields €174,892 gross time-equivalent value, less €19,848 expected errors, €704 inference/retries and €78,000 fixed/semi-fixed costs, plus €65,000 SLA/retention value. Base adoption is **15% / 35% / 60% / 75% by quarter**, averaging 46.25%. Integration is €60,000 upfront, amortised at €20,000/year; reported net value is an annualised model, not year-1 cash profit.
''')+table(['€/year','Pessimistic','Base','Optimistic'],[['Net annual value']+[money(r['net'])for r in results],['Probability','20%','60%','20%'],['Do nothing']+[money(r['dn'])for r in results],['Next-best project']+[money(r['hurdle'])for r in results]])+md(f'''### How sure?
Expected value is **{money(ev)}**, +{money(ev-125000)} versus the base hurdle and +{money(ev-57600)} versus base do-nothing. The dominant guess is 48% time saving on eligible tracing cases. Workbook sensitivity gives €98,251 at 30% and €134,158 at 45%; the interpolated break-even is **41.174%**, rounded up to **41.2%**. Test using paired manual/assisted timing on a frozen 200-case benchmark, including review and fallback time. These are targets, not measured results.

### What if we are wrong?
The pessimistic case loses **€59,828/year**. All seven cost lines are included; financial/data disclosure tail risks remain unpriced beyond operational expected losses. CCO/DPO own the regulatory tail, Ops owns answer quality, Engineering owns deterministic isolation and blocking. A second model cannot guarantee a safe transaction match. Stop drafting on a critical exposure. No real company data or human-validated performance has been supplied.

### Compared to what?
Do nothing assumes 4% natural efficiency gain: **€57,600/year**. The named alternative is the **Merchant Self-Serve Dispute & Reconciliation Portal**, worth **€125,000/year** in Base. The S3 tracing-only MVP does not establish dispute/compliance savings or all €65,000 strategic benefits; a timing pass permits further validation, not the whole business case.

### Build, buy or orchestrate?
**Orchestrate**: weighted scores Build 3.15 / Buy 2.15 / Orchestrate 4.35. Retain permission checks and private read-only retrieval; evaluate hosted model components. At the workbook's €0.92/outcome assumption, vendor usage is €16,090 versus €50,204 comparable internal cost; integration, liability and fit decide. Switch to Buy if an audited suitable connector, approved data terms and liability terms cost <€0.40/outcome. Vendor/API prices rechecked 6 November; USD list prices and workbook EUR assumptions are distinguished in the annex.
''')+'<p class="small">Source: 02_sizing.xlsx, Inputs / Upside / Decision / Build or buy. Formula outputs recomputed from inputs. Original Excel and full assumption register accompany this PDF.</p></div>'
a2+=section('01 · Model, scope and evidence',evidence+md('''The PDF memo is exactly one page. This annex reproduces the model assumptions and recalculates the workbook formulas; it does not replace the required editable Excel workbook.

**Bottom-up equation:** annual volume × category share × eligible share × time saved × adoption × human unit cost − inference/retries − priced errors − fixed costs + other value. “Deflected” rows are time-equivalent tickets for this copilot, not customer tickets resolved autonomously.

**Interpretation limits.** The template applies inference and errors to time-equivalent volume, rather than all assisted conversations. Retain that formula for consistency, but it may underprice usage/errors; at 54,654 eligible assisted conversations in Base, €0.04025 per call would imply €2,200 rather than €704 inference. Re-estimate before spending. Every human review must remain in assisted active time; 0.3 FTE is additional oversight. Gains are capacity value unless hiring, cash or revenue effects are separately evidenced.

Category shares total 94% in Low and 106% in High; Base totals 100%. Historical scenario outputs below preserve those original inputs and expose this limitation. Low leaves 6% unallocated; High is overallocated and must be normalised before an investment decision. They are sensitivity scenarios, not an audited forecast. The €30k retention row is a rounded judgement; the note's detailed multiplication gives €28,800. No extra €220k hiring benefit is added.

**Rollout gates:** Q1 pilot only after tenant, freshness and no-send checks; Q2 only after QA ≥92%, grounding precision ≥98% and zero critical exposures; Q3 only after paired time hurdle and independent review; Q4 only with continued guardrails. These gates are design decisions, not observed rollouts.
'''))
a2+=section('02 · Scenario economics',table(['Year 1','Pessimistic','Base','Optimistic'],[[label]+[fmt(r[key])for r in results]for label,key,fmt in [('Adoption','adopt',lambda x:f'{x:.2%}'),('Gross time-equivalent value','gross',lambda x:money(sum(x))),('Expected operational errors','err',lambda x:money(sum(x))),('Inference + retries','ai',lambda x:money(sum(x))),('Other value','other',money),('Fixed/semi-fixed','fixed',lambda x:money(sum(x))),('Net annual value','net',money),('Do nothing','dn',money),('Named hurdle','hurdle',money)]])+md(f'**Expected value:** 0.2 × ({money(results[0]["net"])}) + 0.6 × {money(base["net"])} + 0.2 × {money(results[2]["net"])} = **{money(ev)}**. Probabilities sum to 1.00. The Decision tab compares EV to the Base do-nothing and Base hurdle. Probability-weighted comparisons are distinct: do-nothing €60,306; hurdle €124,000.')+table(['Base category','Equivalent tickets','Gross value','Errors','AI + retry','Net variable'],[[label,f'{base["eq"][i]:,.2f}',money(base['gross'][i]),money(base['err'][i]),money(base['ai'][i]),money(base['gross'][i]-base['err'][i]-base['ai'][i])]for i,label in enumerate(['Tracing','Disputes','KYC / holds'])]))
a2+=section('03 · Seven cost lines and sensitivity',table(['Cost line','Base €/year','Basis / owner'],[['Tokens and inference',money(sum(base['ai'])),'€0.035 × 1.15 × 17,489.16 equivalents; Engineering'],['Integration','€20,000','€60,000 / 3 years; Engineering'],['Evaluation','€22,000','Dataset + graders; Ops QA'],['Supervision','€16,500','0.3 FTE × €55,000; Ops'],['Monitoring / on-call','€12,000','Engineering / SRE'],['Model re-evaluation','€7,500','3 changes × €2,500; AI lead'],['Expected errors','€19,848','Per category probability × cost × equivalents; Ops / CCO / DPO']])+md('''**Flip-point derivation.** Base net value at tracing time-saving rate x = €26,437.54631 + €239,379.13125 × x. Solve against €125,000: x = 0.4117420478. Use **41.2%** as the conservative rounded requirement. A 10 percentage-point change is worth €23,938/year under this model.

This threshold depends on retaining all other full-scope assumptions. If disputes, compliance or strategic value are excluded, recalculate the business case; the S3 tracing-only pass cannot authorise the full investment.
''')+table(['Tracing saving','Net annual value','Difference vs €125k'],[[(f'{x:.4%}' if abs(x-.4117420478)<1e-8 else f'{x:.1%}'),money(26437.54631+239379.13125*x),money(26437.54631+239379.13125*x-125000)]for x in [.30,.4117420478,.412,.45,.48,.60,.65,.75]]))
# Full register, grouped to avoid splitting section titles from tables.
for start,end,title in [(6,10,'Volume and human cost'),(14,36,'Categories, eligibility, success and errors'),(39,46,'Adoption and variable AI cost'),(49,68,'Fixed costs, comparisons and probabilities')]:
 rows=[];last=''
 for r in range(start,end+1):
  vals=[s.cell(r,c).value for c in range(1,8)]
  if not isinstance(vals[2],(int,float)):continue
  label=vals[0]
  if not label or (isinstance(label,str) and label.startswith('=')):
   if 18<=r<=20:label='Eligible share · '+['Tracing','Disputes','KYC'][r-18]
   elif 22<=r<=24:label='Time saving · '+['Tracing','Disputes','KYC'][r-22]
   elif 26<=r<=28:label='Error rate · '+['Tracing','Disputes','KYC'][r-26]
   elif 30<=r<=32:label='Cost/error · '+['Tracing','Disputes','KYC'][r-30]
   elif 34<=r<=36:label='Include · '+['Tracing','Disputes','KYC'][r-34]
  typ=vals[5]
  if typ=='measured':typ='Course scenario' if r==6 else 'Scenario assumption'
  note=vals[6]
  if r in [18,19,20]:note='Guess; audit planned on 200 cases, not completed. '+str(note)
  if r==45:note='Planning allowance; published-rate calculation rechecked in price annex, not measured spend.'
  rows.append([f'{r}: {label} ({vals[1]})',vals[2],vals[3],vals[4],typ,note])
 a2+=section('04 · Assumption register — '+title,table(['Input / Excel row','Low','Base','High','Source type','Note / validation'],rows),'wide')
b=w['Build or buy'];rows=[[b.cell(r,c).value for c in range(2,8)]for r in range(5,15)]
a2+=section('05 · Build, buy or orchestrate',table(['Question','Weight','Build','Buy','Orchestrate','Reason (planning judgement)'],rows),'wide')
a2+=md('''**Weighted totals:** 3.15 / 2.15 / 4.35; weights sum to 100%. Scores are judgement, not vendor diligence. Historic claims of contractual indemnity, residency or provider capabilities are requirements to verify, not established facts.

**Comparable break-even:** integration amortisation + evaluation + re-evaluation = €49,500/year. Internal cost = €49,500 + €0.04025 × N; vendor cost = €0.92 × N. Equal cost at approximately **56,266 equivalent resolutions/year**. At N = 17,489.16, internal €50,204 versus vendor €16,090: buying is €34,114 cheaper on this limited comparison. Supervision and monitoring stay in both options; connector/platform fees and outcome billing definitions can change the result. A copilot time-equivalent is not automatically a billable vendor outcome.
''')
a2+=section('06 · Price check — 6 November 2026',md('''**Published-rate check, not a replacement for the workbook scenario.** [OpenAI GPT-4o mini model page](https://developers.openai.com/api/docs/models/gpt-4o-mini) lists standard text rates of **$0.15 / million input tokens** and **$0.60 / million output tokens**. The S2 note assumes 4,000 input + 450 output tokens across generator and checker: **$0.00087** per combined pass, or **$0.0010005** with 15% overhead, before extra calls, tooling and tax. This does not validate the proposed checker or production fit. The workbook's **€0.035** is retained as a conservative planning allowance, not a measured API price; no USD/EUR conversion is assumed.

[Intercom public pricing](https://www.intercom.com/pricing) states Fin **from $0.99 per outcome**. The historical workbook uses **€0.92 per resolution**, without a documented dated exchange rate. Keep it as a scenario input, not a current EUR quote. Platform fees, minimums and the exact outcome definition require a vendor quote. Recheck commercial terms and actual call counts before investment.

These checks do not retroactively assert that prices were checked on 16 October. The earlier source mentions of Claude 3.5 Sonnet / GPT-4o-mini are alternatives, not proof of one deployed provider. The published-rate illustration above uses GPT-4o mini only.
'''))
a2+=section('07 · Cost-of-error governance',md('## Session 2'+g2)+md('''## Corrections for the current MVP
A tracing mismatch can also disclose financial data; its cost is not bounded by €15 rework. Cross-tenant exposure, wrong transaction disclosure, invented settlement certainty and unauthorized financial actions are stop events. CCO/DPO assess actual reporting obligations; the historical blanket automatic-notification wording is not an incident assessment. A model score cannot grant access: backend tenant authorization, exact transaction checks and human review are mandatory. Live provider terms, lawful processing and retention remain unapproved requirements.

## Submission checks
Editable workbook, one-page memo and governance are retained in the companion source archive. Formula outputs in this PDF were independently recomputed from the workbook's inputs. Actual commits from at least two members with their own Git accounts remain a separate requirement; no authorship is created by export. Historical scenario shortcomings are disclosed in §1; this PDF is not an audited financial forecast.
'''))
export(2,'Assignment_2_Sizing_Investment_Memo.pdf',a2)

# S3 one-page versions and canvas, followed by full readable supporting material.
def onepage(n,title):
 txt=read(n)
 txt=re.sub(r'^# .*\n','',txt,flags=re.M)
 return '<section class="compact brief"><div class="kicker">ASSIGNMENT 3</div><h1>'+title+'</h1>'+md(txt)+'</section>'
a3=onepage('03_product_brief.md','Product brief · v2')
a3+=onepage('03_ai_lean_canvas.md','AI Lean Canvas · v2')
a3+=onepage('research/brief_v1.md','Product brief · archived v1')
a3+=section('01 · Delivery and requirement status', '<p class="meta">'+TEAM+'</p>'+md('''**Submission date reference:** 8 November 2026 as stated in the Assignment 3 DOCX. PDF packaged 6 November. This package retains the same P2 agent and S2 economic threshold. The brief v2, Lean Canvas and archived brief v1 each occupy one page.

**Outstanding mandatory work:** three genuine 20-minute past-behaviour conversations; two users performing a task thinking aloud; evidence-based user changes in v2; human labelling of all 20 cases; and each member's own authored Git contribution. None can be replaced by formatting or simulated evidence. Initial prototype build duration was not instrumented, so the under-one-hour requirement is not demonstrated.

The design loop recorded below is a desk revision, not a completed participant design loop. The 20 seed cases are presented in full with AI-proposed labels, input, output/action, evidence, handover, segment and origin. They are not claimed to satisfy human labelling until genuine reviewers approve them.
''')+md(read('03_s3_delivery.md').split('## Public demo handover')[0]))
a3+=section('02 · Process, prioritisation and model',md(read('03_design_details.md')),'wide')
a3+=section('03 · User research and design record',md(read('03_user_research.md')))
a3+=section('04 · Clickable prototype and prompt',md(read('03_prototype_link.md')))
a3+=section('05 · Specification skeleton',md(read('spec.md')))
a3+=section('06 · Data audit and governance',md('## Session 3'+g3))
a3+=section('07 · Evaluation recipe and grading',md(read('evals/README_eval_set.md')))
a3+=section('08 · Evidence and policy fixtures',md(read('evals/reference_policy.md')))
rows=list(csv.DictReader((REPO/'evals/eval_set_v0.csv').open()))
for row in rows:
 ident=next(iter(row.values()))
 a3+='<section class="case"><div class="kicker">ASSIGNMENT 3 · EVALUATION SEED</div><h1>Case '+html.escape(ident)+'</h1><p class="small">Synthetic coursework · AI-proposed expected action · Human approval pending</p><dl>'
 for k,v in row.items():
  a3+='<dt>'+html.escape(k.replace('_',' ')).capitalize()+'</dt><dd>'+html.escape(v).replace('\n','<br>')+'</dd>'
 a3+='</dl></section>'
a3+=section('09 · Case-by-case label design review',table(list(next(csv.DictReader((REPO/'evals/label_design_review.csv').open())).keys()),list(csv.reader((REPO/'evals/label_design_review.csv').open()))[1:]),'wide')
a3+=section('10 · Final handover',md('''**Prototype:** [Open FlowAssist](https://deploy-project-product-management.vercel.app). This PDF reproduces the source's 3 November HTTP verification record; it does not claim a fresh visual, integration or performance check. Run `prototype/index.html` locally from the source archive for a buildless synthetic demonstration.

**Sources:** all required Assignment 3 Markdown files, original v1, CSV cases, policy, proposed review register, blank human-review register and prototype assets are retained in `Sources/Assignment_3_sources.zip`. Original file formats remain necessary for the Git submission. This PDF is a readable consolidation.

**Decision:** proceed only with conditional design work. Desirability, model performance, economic savings, human label approvals and production security remain unvalidated. Complete the stated participant and authorship requirements before claiming full compliance with Assignment 3.
'''))
export(3,'Assignment_3_MVP_Brief_and_Design_Loop.pdf',a3)

files1=['README.md','00_pitch.md','01_problem_statement.md','governance.md']
files2=['02_sizing.xlsx','02_investment_memo.md','governance.md']
files3=['03_product_brief.md','03_ai_lean_canvas.md','03_design_details.md','03_user_research.md','03_prototype_link.md','03_s3_delivery.md','spec.md','governance.md','research/brief_v1.md']+[str(p.relative_to(REPO))for p in (REPO/'evals').iterdir()if p.is_file()]+[str(p.relative_to(REPO))for p in (REPO/'prototype').iterdir()if p.is_file()]
for n,files in [(1,files1),(2,files2),(3,files3)]:
 with zipfile.ZipFile(OUT/'Sources'/f'Assignment_{n}_sources.zip','w',zipfile.ZIP_DEFLATED)as z:
  for f in files:z.write(REPO/f,f)
  briefs={1:'Assignment_1_Team_Agent_Problem (1).docx',2:'Assignment_2_Sizing_Investment_Memo (1).docx',3:'Assignment_3_MVP_Brief_and_Design_Loop_due_8_Nov.docx'}
  instruction = ROOT/briefs[n]
  if not instruction.exists():
   instruction = REPO/('course/Assignment_1_Team_Agent_Problem.docx' if n==1 else 'course/Assignment_2_Sizing_Investment_Memo.docx' if n==2 else briefs[n])
  z.write(instruction,'assignment_instructions.docx')
(OUT/'Sources'/'validation.json').write_text(json.dumps(checks,indent=2))
(OUT/'README.md').write_text('''# Assignments — FlowAssist

Trois PDF consolidés, préparés le 6 novembre 2026 à partir des consignes DOCX fournies et des sources de `project-product-management/`.

- Assignment 1 : équipe, problème, diagnostic, hypothèses, pitch et gouvernance.
- Assignment 2 : mémo d’une page en page 1, puis modèle, hypothèses, sept coûts, sensibilité, build/buy et gouvernance. Calculs recomputés depuis Excel ; seuil exact 41,174 %, arrondi à 41,2 %. Les limites du modèle original sont explicites.
- Assignment 3 : brief v2 (page 1), Lean Canvas (page 2), brief v1 (page 3), annexes, spécification, gouvernance et les 20 cas complets.

Les PDF restent en anglais comme les livrables et les consignes. Les archives Sources conservent les formats Markdown, Excel et CSV exigés ainsi que les consignes originales. Les HTML permettent de régénérer les mises en page. Les fichiers originaux du dépôt n’ont pas été modifiés.

## Exigences encore non satisfaites par les éléments disponibles

Assignment 3 : trois conversations réelles, essais à voix haute par deux utilisateurs, modifications attribuables à ces observations et labellisation humaine des cas. Ces éléments ne sont ni inventés ni présentés comme réalisés. La durée initiale de construction du prototype n’est pas démontrée. Les contributions Git personnelles doivent également être vérifiées dans l’historique réel.

Les anciennes affirmations de données internes mesurées sont corrigées par les limites de preuve déjà consignées en S3. Le modèle financier historique présente des limites de répartition des catégories et de facturation par équivalent de temps ; celles-ci sont documentées dans le PDF 2. Ces PDF ne constituent donc pas une attestation de conformité complète aux consignes.
''')
