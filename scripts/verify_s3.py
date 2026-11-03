"""Dependency-free S3 checks. macOS JavaScriptCore checks the local prototype state."""
import csv
import ctypes as C
import re
import json
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((ROOT / 'evals/eval_set_v0.csv').open(newline='')))
assert len(rows) == 20 and {r['id'] for r in rows} == {f'F{i:02}' for i in range(1, 21)}
assert all(all(v.strip() for v in r.values()) for r in rows)
assert sum(r['eligible_for_timing'] == 'yes' for r in rows) == 7
assert all('human validation pending' in r['origin'] for r in rows)
assert all(r['hand_over_to_a_person'] == 'no — L2 approval required' for r in rows if r['eligible_for_timing'] == 'yes')
policies = set(re.findall(r'\| (P\d+) \|', (ROOT / 'evals/reference_policy.md').read_text()))
assert all(set(re.findall(r'\bP\d+\b', r['evidence_or_source'])) <= policies for r in rows)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.elements={}
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
            self.elements[attrs['id']]={'hidden':'hidden' in attrs,'disabled':'disabled' in attrs,'tagName':tag.upper()}
page=Page();page.feed((ROOT/'prototype/index.html').read_text())
assert len(page.ids)==len(set(page.ids))
html=(ROOT/'prototype/index.html').read_text()
assert 'href="styles.css"' in html and 'src="app.js" defer' in html
config=json.loads((ROOT/'vercel.json').read_text())
assert config['outputDirectory']=='dist' and 'prototype/styles.css' in config['buildCommand']
assert (ROOT/'prototype/styles.css').is_file()
js=(ROOT/'prototype/app.js').read_text()
assert set(re.findall(r"\$\('([^']+)'\)",js)) <= set(page.ids)
review=list(csv.DictReader((ROOT/'evals/label_design_review.csv').open(newline='')))
assert len(review)==20 and {r['case_id'] for r in review}=={r['id'] for r in rows}
assert all(r['human_approval']=='not obtained' for r in review)
for path in list(ROOT.glob('03_*.md'))+[ROOT/'README.md',ROOT/'spec.md',ROOT/'prototype/README.md',ROOT/'prototype/verification.md',ROOT/'research/brief_v1.md',ROOT/'evals/README_eval_set.md',ROOT/'prototype/DEPLOYMENT.md']:
    for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        if not re.match(r'https?://|#',link):
            assert (path.parent/link.split('#')[0]).exists(),(path.name,link)
criteria=[]
for name in ['03_product_brief.md','03_design_details.md']:
    criteria.append(next(l for l in (ROOT/name).read_text().splitlines() if l.startswith('> By ')))
assert criteria[0]==criteria[1]
print('PASS: 20 complete unique fixtures, 7 eligible, policy IDs, HTML IDs, document links and identical success criterion.')

# Minimal DOM verifies state transitions; it does not render HTML or simulate a human.
harness=r'''
var checks=0;
function assert(ok,msg){if(!ok)throw Error(msg);checks++;}
class Element {
 constructor(){this.value='';this.checked=false;this.disabled=false;this.hidden=false;this.textContent='';this.children=[];this.events={};this.dataset={};this.classList={add:()=>{},toggle:()=>{}};}
 blur(){this.focused=false;}
 select(){this.selected=true;}
 addEventListener(e,f){this.events[e]=f;}
 setAttribute(k,v){this[k]=v;}
 append(x){this.children.push(x);}
 replaceChildren(){this.children=[];this.textContent='';}
 focus(){this.focused=true;}
 fire(e){if(this.events[e])this.events[e]();}
}
var els={};IDS.forEach(id=>els[id]=Object.assign(new Element(),INITIAL[id]));
var tickets=['ready','ambiguous','sensitive','denied'].map(k=>{var b=new Element();b.dataset.ticket=k;return b;});
var document={events:{},addEventListener(e,f){this.events[e]=f;},getElementById:id=>els[id],createElement:()=>new Element(),querySelectorAll:()=>tickets};
var navigator={};
'''.replace('IDS',json.dumps(page.ids)).replace('INITIAL',json.dumps(page.elements))
checks=r'''
assert($('use-draft').disabled,'initial insertion blocked');
$('review').checked=true;$('review').fire('change');assert($('use-draft').disabled,'review without sources blocked');
$('sources').children[0].fire('click');assert($('use-draft').disabled,'one source insufficient');
$('sources').children[1].fire('click');assert(!$('use-draft').disabled,'all sources plus review enables');
$('use-draft').fire('click');assert($('editor').value.includes('Beneficiary credit is not yet confirmed'),'uncertainty preserved');
$('draft').fire('input');assert(!$('review').checked && $('use-draft').disabled,'edit invalidates review');
$('review').checked=true;$('review').fire('change');$('manual').fire('click');assert($('use-draft').disabled && $('draft-panel').hidden,'manual disables insertion');
$('review').checked=true;$('review').fire('change');assert($('use-draft').disabled,'manual cannot reenable draft');
render('ambiguous');assert($('editor').value==='' && !$('review').checked,'new ticket has isolated editor and no approval');
assert(inspectedSources.size===0,'ticket clears sources');
assert($('draft-panel').hidden && $('use-draft').disabled,'ambiguous suppresses draft');
assert($('gate').textContent.includes('reference is needed'),'actionable gate');
$('escalate').fire('click');assert($('packet').hidden,'reason required');
$('reason').value='Other — see agent note';$('escalate').fire('click');assert($('packet').hidden,'other requires note');
$('reason').value='Ambiguous transaction';$('escalate').fire('click');
assert(!$('packet').hidden,'handover preview available');
assert($('packet').children[0].textContent.includes('Tier-2 payments'),'payment destination');
assert($('packet').children.some(e=>e.textContent.includes('LED-201 (snapshot fetched 2026-11-02T10:00:00Z)') && e.textContent.includes('LED-202')),'timestamped authorized sources');
render('sensitive');assert($('draft-panel').hidden && $('sources').children[0].textContent.includes('No authorized evidence'),'sensitive suppresses data/draft');
$('reason').value='Compliance / sensitive request';$('escalate').fire('click');
assert($('packet').children[0].textContent.includes('Tier-2 compliance'),'compliance destination');
render('denied');assert($('draft-panel').hidden && $('draft').value==='' && examples.denied.sources.length===0,'foreign data absent');
$('reason').value='Access or evidence unavailable';$('escalate').fire('click');
assert($('packet').children.some(e=>e.textContent==='Authorized sources: none'),'denied handover safe');
$('reset').fire('click');assert(current==='ready' && $('packet').hidden && $('editor').value==='' && $('use-draft').disabled,'reset safe');
assert(!manualMode && inspectedSources.size===0,'reset state clean');

// Ticket-specific buffers cannot leak drafts, notes, or approval across tickets.
$('editor').value='Alpha reply';$('editor').fire('input');
$('manual-note').value='Alpha handover';$('manual-note').fire('input');
render('sensitive');assert($('editor').value==='' && $('manual-note').value==='','new merchant has no old text');
$('editor').value='Beta reply';$('editor').fire('input');
render('ready');assert($('editor').value==='Alpha reply' && $('manual-note').value==='Alpha handover','own ticket text restored');
assert(!$('review').checked && inspectedSources.size===0 && $('use-draft').disabled,'restored text grants no approval');
render('sensitive');assert($('editor').value==='Beta reply','other merchant buffer isolated');
render('ready');
$('sources').children[0].fire('click');$('sources').children[1].fire('click');
$('review').checked=true;$('review').fire('change');$('use-draft').fire('click');
assert(!$('replace-confirm').hidden && $('editor').value==='Alpha reply','existing reply never overwritten without choice');
$('cancel-replace').fire('click');assert($('replace-confirm').hidden && $('editor').value==='Alpha reply','cancel keeps reply');
$('use-draft').fire('click');$('confirm-replace').fire('click');
assert($('editor').value===$('draft').value && $('replace-confirm').hidden,'explicit replacement inserts reviewed draft');
$('manual').fire('click');$('resume').fire('click');
assert(!manualMode && !$('draft-panel').hidden && inspectedSources.size===0 && !$('review').checked,'resume requires fresh source inspection and review');
$('search').value='INV-DEMO';$('search').fire('input');
assert(tickets.filter(b=>!b.hidden).length===1 && !tickets[0].hidden,'search includes source reference');
$('search').value='no-match';$('search').fire('input');
assert(!$('search-empty').hidden && $('ticket-count').textContent==='0','empty search explained');
$('search').value='';$('search').fire('input');$('filter-blocked').fire('click');
assert(tickets[0].hidden && tickets.filter(b=>!b.hidden).length===3,'specialist filter');
function key(k,tag='BODY',extra={}){var prevented=false;document.events.keydown({key:k,target:{tagName:tag},preventDefault(){prevented=true;},...extra});return prevented;}
assert(key('j') && current==='ambiguous','keyboard next uses visible filtered tickets');
assert(!key('j','TEXTAREA') && current==='ambiguous','typing does not navigate');
key('k');assert(current==='denied','keyboard previous wraps visible list');
assert(key('/') && $('search').focused,'slash focuses search');
$('shortcuts').fire('click');assert(!$('shortcut-panel').hidden,'shortcut help opens');
key('Escape');assert($('shortcut-panel').hidden,'escape closes help');
render('ready');$('reason').value='Other — see agent note';$('manual-note').value='<script>unsafe</script>';$('escalate').fire('click');
assert($('packet').children.some(e=>e.textContent==='Agent note: <script>unsafe</script>'),'notes inserted as text');
$('manual-note').value='changed';$('manual-note').fire('input');assert($('packet').hidden,'editing note invalidates stale packet');
$('reset').fire('click');assert(buffers.size===0 && $('editor').value==='' && $('manual-note').value==='' && activeFilter==='all' && $('search').value==='','full reset clears all ticket work and filters');
assert($('copy-reply').disabled,'empty reply cannot be copied');
'PASS: '+checks+' prototype state assertions (minimal DOM; no browser rendering).';

'''
lib=C.CDLL('/System/Library/Frameworks/JavaScriptCore.framework/JavaScriptCore')
lib.JSGlobalContextCreate.argtypes=[C.c_void_p];lib.JSGlobalContextCreate.restype=C.c_void_p
lib.JSStringCreateWithUTF8CString.argtypes=[C.c_char_p];lib.JSStringCreateWithUTF8CString.restype=C.c_void_p
lib.JSEvaluateScript.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p,C.c_void_p,C.c_int,C.POINTER(C.c_void_p)];lib.JSEvaluateScript.restype=C.c_void_p
lib.JSValueToStringCopy.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p];lib.JSValueToStringCopy.restype=C.c_void_p
lib.JSStringGetMaximumUTF8CStringSize.argtypes=[C.c_void_p];lib.JSStringGetMaximumUTF8CStringSize.restype=C.c_size_t
lib.JSStringGetUTF8CString.argtypes=[C.c_void_p,C.c_void_p,C.c_size_t]
lib.JSStringRelease.argtypes=[C.c_void_p];lib.JSGlobalContextRelease.argtypes=[C.c_void_p]
ctx=lib.JSGlobalContextCreate(None);source=lib.JSStringCreateWithUTF8CString((harness+'\n'+js+'\n'+checks).encode());exc=C.c_void_p()
result=lib.JSEvaluateScript(ctx,source,None,None,1,C.byref(exc))
value=lib.JSValueToStringCopy(ctx,exc.value or result,None);size=lib.JSStringGetMaximumUTF8CStringSize(value);buf=C.create_string_buffer(size);lib.JSStringGetUTF8CString(value,buf,size)
message=buf.value.decode();lib.JSStringRelease(value);lib.JSStringRelease(source);lib.JSGlobalContextRelease(ctx)
if exc.value:raise AssertionError(message)
print(message)
