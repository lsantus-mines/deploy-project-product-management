"""Verify anonymous HTTP delivery of the exact five current FlowAssist assets.

This does not render a browser or establish backend security/model quality.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://deploy-project-product-management.vercel.app/'
ASSETS = ['index.html', 'styles.css', 'data.js', 'engine.js', 'app.js']


def check(name):
    path = '' if name == 'index.html' else name
    request = Request(BASE + path, headers={'Cache-Control': 'no-cache'})
    try:
        with urlopen(request, timeout=25) as response:
            actual = response.read()
            status = response.status
        expected = (ROOT / 'prototype' / name).read_bytes()
        matches = status == 200 and actual == expected
        return name, matches, f'HTTP {status}; SHA256 {hashlib.sha256(actual).hexdigest()[:12]}'
    except Exception as error:
        return name, False, str(error)


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=5) as pool:
        results = list(pool.map(check, ASSETS))
    for name, passed, detail in results:
        print(f'{"PASS" if passed else "FAIL"}: {name}: {detail}')
    if not all(passed for _, passed, _ in results):
        raise SystemExit('Production is not yet serving all current assets.')
    print('PASS: anonymous production delivery matches all five local runtime assets.')
