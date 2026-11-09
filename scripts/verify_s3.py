"""S3 artifact checks plus current application domain/interaction tests (Node.js required)."""
import csv
import re
import json
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((ROOT / 'evals/eval_set_v0.csv').open(newline='')))
assert len(rows) == 50 and {r['id'] for r in rows} == {f'F{i:02}' for i in range(1, 51)}
assert all(all(v.strip() for v in r.values()) for r in rows)
assert sum(r['eligible_for_timing'] == 'yes' for r in rows) == 15
assert all('human validation pending' in r['origin'] for r in rows)
assert all(r['hand_over_to_a_person'] == 'no — L2 approval required' for r in rows if r['eligible_for_timing'] == 'yes')
policies = set(re.findall(r'\| (P\d+) \|', (ROOT / 'evals/reference_policy.md').read_text()))
assert all(set(re.findall(r'\bP\d+\b', r['evidence_or_source'])) <= policies for r in rows)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.elements={}; self.stack=[]; self.scripts=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag == 'script': self.scripts.append(attrs.get('src'))
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: self.stack.append(tag)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
            self.elements[attrs['id']]={'hidden':'hidden' in attrs,'disabled':'disabled' in attrs,'tagName':tag.upper()}
    def handle_endtag(self, tag):
        if tag in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: return
        assert self.stack and self.stack[-1] == tag, (tag, self.stack[-6:])
        self.stack.pop()
page=Page();page.feed((ROOT/'prototype/index.html').read_text())
assert len(page.ids)==len(set(page.ids))
assert not page.stack
assert page.scripts == ['data.js','engine.js','app.js']
html=(ROOT/'prototype/index.html').read_text()
assert 'href="styles.css"' in html and 'src="app.js" defer' in html
config=json.loads((ROOT/'vercel.json').read_text())
assert config['outputDirectory']=='dist'
for asset in ['styles.css','data.js','engine.js','app.js']:
    assert f'prototype/{asset}' in config['buildCommand'] and (ROOT/'prototype'/asset).is_file()
assert (ROOT/'prototype/styles.css').is_file()
js=(ROOT/'prototype/app.js').read_text()
assert set(re.findall(r"\$\(['\"]([^'\"]+)['\"]\)",js)) <= set(page.ids)
review=list(csv.DictReader((ROOT/'evals/label_design_review.csv').open(newline='')))
assert len(review)==20 and {r['case_id'] for r in review}=={r['id'] for r in rows[:20]}
assert all(r['human_approval']=='not obtained' for r in review)
for path in list(ROOT.glob('03_*.md'))+list((ROOT/'docs').glob('*.md'))+[ROOT/'README.md',ROOT/'spec.md',ROOT/'prototype/README.md',ROOT/'prototype/verification.md',ROOT/'research/brief_v1.md',ROOT/'evals/README_eval_set.md',ROOT/'prototype/DEPLOYMENT.md']:
    for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        if not re.match(r'https?://|#',link):
            assert (path.parent/link.split('#')[0]).exists(),(path.name,link)
criteria=[]
for name in ['03_product_brief.md','03_design_details.md']:
    criteria.append(next(l for l in (ROOT/name).read_text().splitlines() if l.startswith('> By ')))
assert criteria[0]==criteria[1]
print('PASS: 50 complete unique fixtures, 15 proposed eligible, policy IDs, HTML IDs, document links and identical success criterion.')

# Execute current domain + interaction scenarios with the installed Node runtime.
import subprocess
subprocess.run(['node', '--test', str(ROOT/'scripts/test_app.cjs')], check=True, cwd=ROOT)
