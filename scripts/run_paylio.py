"""Replay the unmodified supplied starter; needs pandas and scikit-learn."""
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
result = subprocess.run([sys.executable, '_backup_run/prototype/evals.py'],
                        cwd=ROOT/'paylio-copilot-demo', capture_output=True, text=True)
if result.returncode:
    sys.stderr.write(result.stderr)
    raise SystemExit(result.returncode)
out = ROOT/'docs/evidence/s4/paylio-run.txt'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(result.stdout)
print(result.stdout)
print('Starter heuristic only; sendability is not an independent human judgement.')
