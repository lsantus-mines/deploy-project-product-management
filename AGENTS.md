# Repository collaboration instructions

## Source and publication repositories

- Develop and push product changes to `BenjaminAHS/project-product-management`, branch `main`.
- Vercel builds the publication copy `lsantus-mines/deploy-project-product-management`, branch `main`.
- After every successful primary `main` push, run `python scripts/deploy/sync_deploy.py` and confirm its push/no-change result. This preserves the copy’s separate history. Do not force-push or configure two push URLs: the histories are different.
- The GitHub workflow also synchronizes primary pushes by all teammates using the configured `DEPLOY_REPO_TOKEN` Actions secret (a successful push-triggered run is recorded in the deployment guide). Confirm each relevant run rather than assuming success. If the local fallback loses a race to the workflow, rerun from a fresh clone and confirm no differences; never force-push.
- Workflow definitions are excluded from the snapshot. Preserve destination-owned workflows. Never read, print or commit credential values.
- Verify changes with `make ci` (lint, Python + Node tests, JS/Python engine parity, regression, attack set). `python scripts/verify/verify_s3.py` still runs the interface checks alone.
- The server (`api/index.py`, `flowassist/engine.py`) is the authority; any rule change goes in both engines, and `tests/test_parity.py` must stay green. After editing `prototype/data.js`, run `make export-data`. Metrics stay local (`metrics/`, git-ignored); never add third-party analytics or send ticket text in events. Verify synchronization changes with `python scripts/deploy/test_sync_deploy.py` (local temporary Git repositories; no network).
- Hosting and synchronization setup: `docs/DEPLOYMENT.md`. Do not claim a live deployment or public URL until verified.

## Current application

- The v0.8 public demo is in `prototype/` (one guided flow in three steps): `data.js` supplies synthetic fixtures, `engine.js` holds pure domain logic, and `app.js` manages the workflow. Keep every runtime asset in the Vercel copy command.
- `scripts/verify/test_app.cjs` tests domain and interaction behavior using Node’s built-in test runner. The DOM harness is not browser/rendering evidence.
- Preserve the distinction between local deterministic checks and the target model-based evaluator. Do not claim bank/Zendesk connections, server-side tenant security or causal time savings from the demo. See `docs/PRODUCT_COVERAGE.md`.
