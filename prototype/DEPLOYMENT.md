# FlowAssist — Vercel deployment handover

**Updated: 3 November 2026. Status: configuration ready; publication pending.**

## Repository and deployment ownership

The shared source repository is [BenjaminAHS/project-product-management](https://github.com/BenjaminAHS/project-product-management). Lenny is a contributor, not the repository owner. The owner is arranging to make it public; no visibility change is asserted as completed in this record. The Vercel project owner and production domain are not yet confirmed.

The preferred route is to deploy the shared repository using a Vercel account/team with access to it. If the repository cannot be selected from a contributor’s account, the owner can perform the import or configure the required GitHub access. Once the repository is public, a team member can alternatively deploy a fork/copy on their own account; that creates a separate source to maintain and is not automatically synchronized with the shared repository.

## Deployment settings

Import the selected repository in Vercel. Keep these settings:

| Setting | Value |
|---|---|
| Root Directory | Repository root (`.`), not `prototype/` |
| Framework Preset | Other (`framework: null`) |
| Install Command | Empty; no dependencies |
| Build Command | `mkdir -p dist && cp prototype/index.html prototype/app.js prototype/styles.css dist/` |
| Output Directory | `dist` |
| Environment variables | None |
| Entry route | `/` |

The tracked [vercel.json](../vercel.json) contains these build settings. The deployment output contains only `index.html`, `app.js` and `styles.css`; course files, research notes, evaluation data and the Paylio starter are not copied into the website. Local `.vercel/` metadata and `dist/` are ignored by Git.

Repository visibility and website access are separate. Use the production domain for sharing and verify that production Deployment Protection permits visitors without a Vercel login. Do not assume that a preview URL is publicly accessible.

## Release acceptance

After deployment succeeds:

1. Open the production URL in a private browser window without a Vercel session. The inbox must load without an authentication screen.
2. On DEMO-01, inspect both sources, confirm review and insert the draft in the editor. Editing the draft must clear review. Existing text in the editor must require confirmation before replacement. No message is sent.
3. On DEMO-02, confirm the missing-reference explanation and the blocked draft; select a reason and inspect the timestamped handover.
4. On DEMO-03, confirm Tier-2 compliance routing. On DEMO-04, confirm that no transaction evidence is exposed.
5. Search/filter tickets, switch between merchants and confirm that each restores only its own text while approval resets. Check a narrow/mobile viewport and keyboard navigation. Record actual findings rather than assuming the structural checks establish rendering/accessibility.
6. Record the production domain, Vercel project owner, deployed source commit and check date below; update the root README and `03_prototype_link.md` together.

| Release evidence | Current status |
|---|---|
| Source | Shared repository above; Vercel configuration tracked |
| Repository made public | Awaiting owner action / confirmation |
| Vercel project owner | Not confirmed |
| Successful deployment and deployed commit | Not confirmed |
| Production URL | Not available yet |
| Anonymous access and browser checks | Not performed |

## Local checks and demo scope

Run `python scripts/verify_s3.py` from the repository root on macOS. The latest completed run passed the structural checks and 44 scripted interaction assertions. See [verification limits](verification.md).

Hosting changes access to the same S3 demo; it adds no live model, bank connector, Zendesk integration, persistent storage, customer sending or fund action. All four demonstration tickets remain synthetic. For immediate local use, open `prototype/index.html`, or run `python -m http.server 8000 --bind 127.0.0.1` at the repository root and visit `http://127.0.0.1:8000/prototype/`.

Configuration reference: [official Vercel documentation](https://vercel.com/docs/project-configuration/vercel-json).
