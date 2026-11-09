"""Build Lenny's offline review page; no engine run, labels or approvals are generated."""
import argparse
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build(destination):
    source = ROOT / 'evals/eval_set_v1.csv'
    with source.open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        columns, rows = reader.fieldnames, list(reader)
    ids = {f'V{i:03}' for i in [*range(1, 41), *range(197, 201)]}
    selected = [row for row in rows if row['id'] in ids]
    assert len(selected) == 44
    buffer = io.StringIO(newline='')
    writer = csv.DictWriter(buffer, fieldnames=columns)
    writer.writeheader()
    writer.writerows(selected)
    bundle = dict(member='Lenny', cases=buffer.getvalue(),
                  proposals=(ROOT / 'evals/proposals_v1_Lenny.csv').read_text(encoding='utf-8'))
    # Escape HTML delimiters so fixture text can never close the script element.
    payload = json.dumps(bundle, ensure_ascii=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    html = (ROOT / 'evals/labeller.html').read_text(encoding='utf-8')
    html = html.replace('<script>', '<script>globalThis.FLOW_REVIEW_BUNDLE = ' + payload + ';</script>\n<script>', 1)
    Path(destination).write_text(html, encoding='utf-8')
    print(f'Offline review ready: {destination} (44 inputs, 40 AI proposals, zero approvals)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', help='Destination HTML file; open directly in a browser')
    build(parser.parse_args().output)
