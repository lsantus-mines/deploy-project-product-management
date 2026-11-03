# Repository collaboration instructions

## Source and publication repositories

- Develop and push product changes to `BenjaminAHS/project-product-management`, branch `main`.
- Vercel builds the publication copy `lsantus-mines/deploy-project-product-management`, branch `main`.
- After every successful primary `main` push, run `python scripts/sync_deploy.py` and confirm its push/no-change result. This preserves the copy’s separate history. Do not force-push or configure two push URLs: the histories are different.
- The GitHub workflow also synchronizes primary pushes by all teammates using the configured `DEPLOY_REPO_TOKEN` Actions secret (a successful push-triggered run is recorded in the deployment guide). Confirm each relevant run rather than assuming success. If the local fallback loses a race to the workflow, rerun from a fresh clone and confirm no differences; never force-push.
- Workflow definitions are excluded from the snapshot. Preserve destination-owned workflows. Never read, print or commit credential values.
- Verify app changes with `python scripts/verify_s3.py` (Python + Node.js, no test dependencies). Verify synchronization changes with `python scripts/test_sync_deploy.py` (local temporary Git repositories; no network).
- Hosting and synchronization setup: `prototype/DEPLOYMENT.md`. Do not claim a live deployment or public URL until verified.

## Current application

- The v0.4 public demo is in `prototype/`: `data.js` supplies synthetic fixtures, `engine.js` holds pure domain logic, and `app.js` manages the workflow. Keep every runtime asset in the Vercel copy command.
- `scripts/test_app.cjs` tests domain and interaction behavior using Node’s built-in test runner. The DOM harness is not browser/rendering evidence.
- Preserve the distinction between local deterministic checks and the target model-based evaluator. Do not claim bank/Zendesk connections, server-side tenant security or causal time savings from the demo. See `docs/PRODUCT_COVERAGE.md`.
