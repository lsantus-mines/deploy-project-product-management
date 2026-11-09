"""Check eval-set v1 structure and label completeness. Never runs the engine on V001–V200."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(name):
    with (ROOT / name).open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


rows = read_csv('evals/eval_set_v1.csv')
fixtures = json.loads((ROOT / 'evals/fixtures_v1.json').read_text(encoding='utf-8'))
ids = [f'V{i:03}' for i in range(1, 201)]
assert sorted(r['id'] for r in rows) == sorted(f['id'] for f in fixtures) == ids
assert sorted(r['case_id'] for r in read_csv('evals/label_review_v1.csv')) == ids
assert sorted(r['id'] for r in read_csv('evals/eval_set_v1_design.csv')) == ids
assert not set(ids) & {r['id'] for r in read_csv('evals/eval_set_v0.csv')}
refs = [t['reference'] for f in fixtures for t in f['data']['transactions']]
assert len(refs) == len(set(refs)), 'duplicate reference across the set'
assert all(f['ticket']['id'] == f['id'] for f in fixtures)

LABELS = ['expected_output_or_action', 'hand_over_to_a_person', 'case_type', 'eligible_for_timing']
done = [r for r in rows if all(r[k].strip() for k in LABELS)]
partial = [r['id'] for r in rows if any(r[k].strip() for k in LABELS) and r not in done]
assert not partial, f'partially labelled cases: {partial[:10]}'
assert all(r['case_type'] in {'easy', 'hard', 'adversarial', 'out_of_scope'} for r in done)
assert all(r['eligible_for_timing'] in {'yes', 'no'} for r in done)
# A results file before labels are complete means the set was exposed before freezing.
assert (ROOT / 'evals/results_v1.json').exists() is False or len(done) == 200, 'v1 was run before labelling finished'
print(f'PASS: 200 v1 inputs aligned, unique references, no overlap with v0. Labelled: {len(done)}/200.')
