"""Build the concise S4 PDF, source bundle and layout validation independently."""
from pathlib import Path
import csv
import hashlib
import json
import zipfile
import os
import tempfile
import cffi
import markdown

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Assignments'
SRC = OUT / 'Sources'
# Match the existing PDF toolchain without regenerating historical S1–S3 files.
original_dlopen = cffi.FFI.dlopen
lib = Path('/Applications/Inkscape.app/Contents/Resources/lib')
libs = {'libpango-1.0-0':'libpango-1.0.0.dylib','libgobject-2.0-0':'libgobject-2.0.0.dylib','libharfbuzz-0':'libharfbuzz.0.dylib','libharfbuzz-subset-0':'libharfbuzz-subset.0.dylib','libfontconfig-1':'libfontconfig.1.dylib','libpangoft2-1.0-0':'libpangoft2-1.0.0.dylib'}
if lib.exists():
    cffi.FFI.dlopen = lambda self,name,*a,**k: original_dlopen(self,str(lib/libs[name]) if name in libs else name,*a,**k)
    fontdir = Path(tempfile.gettempdir()) / 'flowassist-s4-fonts'
    fontdir.mkdir(exist_ok=True)
    config = fontdir/'fonts.conf'
    config.write_text('<fontconfig><dir>/System/Library/Fonts</dir><dir>/Library/Fonts</dir><cachedir>'+str(fontdir/'cache')+'</cachedir></fontconfig>')
    os.environ['FONTCONFIG_FILE'] = str(config)
from weasyprint import HTML

css = '''
@font-face{font-family:Body;src:url("file:///System/Library/Fonts/Supplemental/Arial.ttf")}
@font-face{font-family:Body;src:url("file:///System/Library/Fonts/Supplemental/Arial Bold.ttf");font-weight:700}
@page{size:A4;margin:16mm 16mm 16mm;@bottom-left{content:"FLOWASSIST · ASSIGNMENT 4 · 9 NOVEMBER 2026";font:7pt Body;color:#567079}@bottom-right{content:counter(page) " / " counter(pages);font:7pt Body;color:#567079}}
body{font:8.7pt/1.27 Body,Arial,sans-serif;color:#243644;margin:0}
h1{font-size:21pt;line-height:1.12;color:#123c45;margin:0 0 4mm}
h2{font-size:11.5pt;color:#146e76;margin:3mm 0 1.5mm;break-after:avoid}
p{margin:0 0 2.4mm}a{color:#08747c;text-decoration:none;overflow-wrap:anywhere}
table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:7.6pt;line-height:1.23;margin:2mm 0 3mm}
th{background:#153e4c;color:white}th,td{text-align:left;vertical-align:top;padding:1.5mm;border-bottom:.5pt solid #d9e3e7;overflow-wrap:anywhere}
tr{break-inside:avoid}tbody tr:nth-child(even){background:#eff5f5}
ul{padding-left:4.5mm;margin:1.5mm 0 2.5mm}li{margin-bottom:1.4mm}
code{font-size:8pt;overflow-wrap:anywhere}pre{white-space:pre-wrap;background:#eff5f5;padding:3mm;font:8pt/1.25 monospace;overflow-wrap:anywhere}
.diagram{font:8pt/1.18 monospace;padding:3mm;margin:2mm 0 3mm}
.kicker{font-size:8pt;letter-spacing:1.2pt;font-weight:bold;color:#16848a;margin-bottom:3mm}
.meta{font-size:8pt;color:#526b77;margin-bottom:4mm}
section{break-before:page}section:first-child{break-before:auto}
'''
content = (SRC/'assignment4_content.md').read_text()
pages = content.split('<!-- PAGE -->')
body = ''.join('<section>'+markdown.markdown(p,extensions=['tables','fenced_code','sane_lists'])+'</section>' for p in pages)
html = '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Assignment 4 — FlowAssist</title><style>'+css+'</style></head><body>'+body+'</body></html>'
(SRC/'Assignment_4.html').write_text(html)
doc = HTML(string=html,base_url=str(ROOT)).render()
assert len(doc.pages)==4, f'Expected four concise pages, got {len(doc.pages)}'
overflow=[]
for i,page in enumerate(doc.pages,1):
    for box in page._page_box.descendants():
        if getattr(box,'text',None) and box.position_y < page.height-60:
            if box.position_x+box.width > page.width-40 or box.position_y+box.height > page.height-35:
                overflow.append([i,box.text[:80]])
assert not overflow,overflow
pdf=OUT/'Assignment_4_Prototype_and_Architecture.pdf'
doc.write_pdf(pdf)
rows=list(csv.DictReader((ROOT/'evals/eval_set_v0.csv').open()))
assert len(rows)==50
results=json.loads((ROOT/'evals/results_v0.json').read_text())
assert results['summary']['stateMatches']==50 and results['summary']['drafts']==15
assert '35/50' in content
paths=['04_architecture.md','04_s4_delivery.md','spec.md','governance.md','03_product_brief.md','03_ai_lean_canvas.md','03_user_research.md','03_prototype_link.md','AGENTS.md','vercel.json','Assignment_4_Prototype_and_Architecture_due_15_Nov (1).docx']
paths += [str(p.relative_to(ROOT)) for folder in ['prototype','evals','S4_templates'] for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
paths += ['scripts/test_app.cjs','scripts/verify_s3.py','scripts/verify_s4.py','scripts/eval_s4.cjs','scripts/run_paylio.py','docs/evidence/s4/paylio-run.txt','Assignments/Sources/assignment4_content.md','Assignments/Sources/build_assignment4.py']
with zipfile.ZipFile(SRC/'Assignment_4_sources.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in sorted(set(paths)):
        z.write(ROOT/name,name)
validation={'file':pdf.name,'pages':len(doc.pages),'cases':len(rows),'overflow':overflow,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'source': 'assignment4_content.md','build':'/opt/anaconda3/bin/python Assignments/Sources/build_assignment4.py'}
(SRC/'validation_s4.json').write_text(json.dumps(validation,indent=2)+'\n')
print(json.dumps(validation,indent=2))
