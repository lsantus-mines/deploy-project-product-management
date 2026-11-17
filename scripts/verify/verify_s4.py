"""Validate S4 artifacts and rerun the deterministic development evaluation."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
def read_csv(name):
    with (ROOT / name).open(newline='') as stream:
        return list(csv.DictReader(stream))

rows = read_csv('evals/eval_set_v0.csv')
fixtures = json.loads((ROOT / 'evals/v0/fixtures_v0.json').read_text())
ids = [f'F{i:02}' for i in range(1, 51)]
assert [r['id'] for r in rows] == [f['id'] for f in fixtures] == ids
for name in ['evals/v0/label_review.csv', 'evals/v0/grader_reviews.csv']:
    assert [r['case_id'] for r in read_csv(name)] == ids
assert all(f['expectedState'] in {'draft_ready', 'human_only', 'context_only'} for f in fixtures)
for name in ['04_architecture.md', 'docs/04_s4_delivery.md', 'evals/report_v0.md']:
    assert (ROOT / name).is_file(), name
for suffix, engine in [('results_baseline_v0.json', 'evals/v0/engine_baseline_v0.js'),
                       ('results_v0.json', 'prototype/engine.js')]:
    subprocess.run(['node', 'scripts/eval/eval_s4.cjs'] + (['--baseline'] if 'baseline' in suffix else []), check=True, cwd=ROOT)
    result = json.loads((ROOT / 'evals' / 'v0' / suffix).read_text())
    for key, name in [('engineSHA256', engine), ('fixtureSHA256', 'evals/v0/fixtures_baseline_v0.json' if 'baseline' in suffix else 'evals/v0/fixtures_v0.json')]:
        assert result[key] == hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    assert [r['id'] for r in result['results']] == ids
    # Critical safety invariants; don't equate state agreement with human quality.
    assert result['summary']['foreignSources'] == 0
    assert result['summary']['humanOnlyDrafts'] == 0
print('PASS: S4 artifact alignment, 50 review slots, reproducible hashes and local safety invariants. Human grading pending.')
