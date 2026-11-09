# FlowAssist — Vercel deployment handover

**Updated: 9 November 2026. S4 source push and publication snapshot verified; latest successful HTTP asset verification remains the 3 November release.**

## Latest Git release evidence · 9 November 2026

- Primary `main` push succeeded for `034267cbc22a`.
- A fresh publication checkout contained `8a8a2cf75f1076b507bc55cf163c61b09b1c9d26` (`Sync primary main at 034267cbc22a`).
- `python3 scripts/sync_deploy.py --checkout /private/tmp/flowassist-deploy-034267c` reported **0 changed, 0 removed; workflows preserved**. The temporary path is local evidence, not a required setup path for other machines.
- The initial local synchronization attempt failed DNS; retrying with a fresh direct Git clone allowed the snapshot comparison. The matching publication commit confirms the copy; the Actions run itself was not inspected because `gh` was unauthenticated.
- `python3 scripts/verify_production.py` could not resolve the production host. The latest successful anonymous HTTP/asset evidence remains **3 November**, below. Do not infer an updated Ready deployment or current byte parity from the Git comparison alone.

The following initial setup and release evidence is historical unless explicitly dated otherwise.

## Repository and deployment ownership

- **Source of truth:** [BenjaminAHS/project-product-management](https://github.com/BenjaminAHS/project-product-management), branch `main`.
- **Vercel source copy:** [lsantus-mines/deploy-project-product-management](https://github.com/lsantus-mines/deploy-project-product-management), branch `main`, owned by Lenny’s GitHub account.
- **Verified on 3 November:** the deployment copy’s initial commit `e9cd7ea` contains the same tracked files as primary commit `c10cc20` (interface v0.3). The repositories have separate histories; synchronization therefore creates ordinary snapshot commits instead of force-pushing primary history.
- **Vercel status:** existing project `deploy-project-product-management`, owner Team Montagne; production deployment `dpl_4isLr4HL3Y1s1a3DgVSzm6rgf61g` is Ready. [Public demo](https://deploy-project-product-management.vercel.app) responded with anonymous HTTP 200 on 3 November 2026. All five v0.4 runtime assets match local files byte for byte; `python scripts/verify_production.py` repeats these anonymous checks.
- **Synchronization evidence:** local fallback successfully copied primary `a1359fe` into deployment snapshot `cd4ecbc`, preserving initial history and excluding workflow definitions. This does not establish a successful GitHub Actions run.

Keep making product changes in the primary repository. The deployment copy is a publication target; do not develop there independently.

## Automatic synchronization after primary pushes

The [GitHub workflow](../.github/workflows/sync-deploy.yml) triggers on every push to primary `main`, and can be rerun manually from Actions. Runs are serialized and read the latest primary `main` at execution time so the deployment copy converges on the current source. It runs only in the primary repository, not on forks/copies.

The workflow copies committed files and deletions into the deployment repository and makes a normal commit/push. It preserves the destination history and destination-owned `.github/workflows/` files. Workflow definitions are excluded from cross-repository copying, so the destination credential requires only Contents write permission. The sync fails on an unexpected repository, dirty checkout, unsafe path/symlink or concurrent remote update; it never force-pushes. Secrets and local `.git` metadata are never copied. A no-change run creates no commit.

**Guide français pas à pas : [activer le secret Actions](../docs/ACTIVER_SYNC_GITHUB.md).**

**Verified status:** [push-triggered workflow run](https://github.com/BenjaminAHS/project-product-management/actions/runs/41667205280) succeeded for primary `e33deb3`. The secret is now effective. The following instructions remain for renewal or reconfiguration.

**One-time activation:** the owner or an authorized collaborator of the primary repository must add an Actions repository secret named `DEPLOY_REPO_TOKEN` at [primary repository secrets](https://github.com/BenjaminAHS/project-product-management/settings/secrets/actions). Use a fine-grained token from `lsantus-mines`, limited to `deploy-project-product-management`, with **Contents: Read and write**. Enter the token in GitHub’s secret form, not source files or chat. If this secret is absent or expires, the workflow explicitly fails with a setup message. GitHub’s default workflow token does not provide this cross-repository write access. See [GitHub token guidance](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).

After activation, push to primary `main` (or rerun the workflow), confirm the Actions run succeeds, and check the new snapshot commit on deployment `main`. Vercel should be connected to that repository and branch; verify its deployment separately.

**Local fallback, also used by agents after a primary push:**

```sh
python scripts/sync_deploy.py --dry-run
python scripts/sync_deploy.py
```

These commands use the existing Git credential helper, clone the deployment repository into a temporary directory, and synchronize the current committed `HEAD`. Uncommitted source edits are excluded. Publish primary `main` first. Local fallback does not replace the workflow for pushes by teammates.

## Deployment settings

Import the selected repository in Vercel. Keep these settings:

| Setting | Value |
|---|---|
| Root Directory | Repository root (`.`), not `prototype/` |
| Framework Preset | Other (`framework: null`) |
| Install Command | Empty; no dependencies |
| Build Command | `mkdir -p dist && cp prototype/index.html prototype/app.js prototype/data.js prototype/engine.js prototype/styles.css dist/` |
| Output Directory | `dist` |
| Environment variables | None |
| Entry route | `/` |

The tracked [vercel.json](../vercel.json) contains these build settings. The deployment output contains only `index.html`, `styles.css`, `data.js`, `engine.js` and `app.js`; course files, research notes, evaluation data and the Paylio starter are not copied into the website. Local `.vercel/` metadata and `dist/` are ignored by Git.

Repository visibility and website access are separate. Use the production domain for sharing and verify that production Deployment Protection permits visitors without a Vercel login. Do not assume that a preview URL is publicly accessible.

## Release acceptance

After deployment succeeds:

1. Open the production URL in a private browser window without a Vercel session. The inbox must load without an authentication screen.
2. On DEMO-01, inspect both sources, confirm review and insert the draft in the editor. Editing the draft must clear review. Existing text in the editor must require confirmation before replacement. No message is sent.
3. On DEMO-02, confirm the missing-reference explanation and the blocked draft; select a reason and inspect the timestamped handover.
4. On DEMO-03, confirm Tier-2 compliance routing. On DEMO-04, confirm that no transaction evidence is exposed.
5. Search/filter tickets, switch between merchants and confirm that each restores only its own text while approval resets. Check a narrow/mobile viewport and keyboard navigation. Record actual findings rather than assuming the structural checks establish rendering/accessibility.
6. Record the production domain, Vercel project owner, deployed source commit and check date below; update the root README and `03_prototype_link.md` together.

| Historical release evidence (3 November) | Recorded status |
|---|---|
| Source | Shared repository above; Vercel configuration tracked |
| Deployment repository | `lsantus-mines/deploy-project-product-management`, branch `main`; copy contents verified |
| Automatic sync | Verified successful push-triggered run for primary `e33deb3`; linked above |
| Vercel project owner | Team Montagne; CLI authenticated as `lsantus-mines` |
| Successful deployment and deployed commit | Ready: `dpl_4isLr4HL3Y1s1a3DgVSzm6rgf61g`; exact deployed Git SHA not exposed in inspected metadata; all five v0.4 app assets match source `e33deb3` |
| Production URL | https://deploy-project-product-management.vercel.app |
| Anonymous access and browser checks | Anonymous HTTP 200 and all five v0.4 asset bytes verified; rendered UI/mobile/clipboard checks unperformed |

## Local checks and demo scope

Run `python scripts/verify_s3.py` from the repository root with Python and Node.js. The current run passes the artifact checks and 32 domain/interaction scenarios; `python3 scripts/verify_s4.py` also reproduces the 50-case development evaluation. See [verification limits](verification.md).

Hosting changes access to the same S3 demo; it adds no live model, bank connector, Zendesk integration, shared backend storage, customer sending or fund action. The v0.4 adds per-tab sessionStorage for synthetic cases, local analysis, lifecycle and audit/timing. All ten starting cases remain synthetic. For immediate local use, open `prototype/index.html`, or run `python -m http.server 8000 --bind 127.0.0.1` at the repository root and visit `http://127.0.0.1:8000/prototype/`.

Configuration reference: [official Vercel documentation](https://vercel.com/docs/project-configuration/vercel-json).
