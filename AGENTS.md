# Repository collaboration instructions

## Source and publication repositories

- Develop and push product changes to `BenjaminAHS/project-product-management`, branch `main`.
- Vercel builds the publication copy `lsantus-mines/deploy-project-product-management`, branch `main`.
- After every successful primary `main` push, run `python scripts/sync_deploy.py` and confirm its push/no-change result. This preserves the copy’s separate history. Do not force-push or configure two push URLs: the histories are different.
- The GitHub workflow also synchronizes primary pushes by all teammates once the primary repository’s `DEPLOY_REPO_TOKEN` Actions secret is configured. Do not assume it ran successfully; report any setup/authentication failure.
- Workflow definitions are excluded from the snapshot. Preserve destination-owned workflows. Never read, print or commit credential values.
- Verify app changes with `python scripts/verify_s3.py` on macOS. Verify synchronization changes with `python scripts/test_sync_deploy.py` (local temporary Git repositories; no network).
- Hosting and synchronization setup: `prototype/DEPLOYMENT.md`. Do not claim a live deployment or public URL until verified.
