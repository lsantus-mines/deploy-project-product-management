# v1 label submissions

Lenny submitted 44 completed rows on 9 November 2026: V001–V040 and V197–V200. The other members' exports have not been received in this directory. These are submitted labels awaiting the full-team merge, not a frozen 200-case benchmark.

- `labels_v1_Lenny.csv`: canonical merge input, including the V197 correction and accurate AI provenance.
- `raw/labels_v1_Lenny.csv`: unchanged browser export, archived for traceability. Do not pass raw exports to the merge script.

V001–V040 were AI-proposed and accepted through the review page. V198–V200 were proposed in the chat and entered by Lenny; their original export incorrectly described them as written by hand. The canonical copy corrects provenance only for those three cases, preserving all answers. V197 mistakenly repeated the Polish-language answer from V040 although its ticket is in English. After this mismatch was explained, Lenny acknowledged the mistake; the canonical copy corrects it with AI assistance: unique own reference, fresh sources, consistent gross/fee/net and credited status. No prototype output was consulted or produced.

All 44 canonical rows therefore disclose AI assistance. In particular, V197–V200 are not unaided independent labels: report their agreement separately from any unaided-human agreement. The raw agreement printed by the current merge script does not distinguish assisted and unaided judgements.

Raw export SHA-256: `402e51dca9e19dc47516be0ca5a0286199d779b236a7b94dcf5a7bd9edd04ba3`.

Once every member has submitted an export, run from the repository root:

```sh
python3 scripts/merge_labels_v1.py evals/submissions/labels_v1_*.csv
```

The script requires coverage of all 200 cases. Resolve disagreements before freezing `eval-v1`; do not run the engine before that freeze.
