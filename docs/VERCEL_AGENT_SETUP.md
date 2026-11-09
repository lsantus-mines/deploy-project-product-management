# Vercel agent setup · historical configuration verified 3 November 2026

Current release evidence is maintained in [the deployment guide](../prototype/DEPLOYMENT.md): S4 Git snapshot synchronization was confirmed on 9 November; updated HTTP delivery was verified the same day.

The requested [official onboarding playbook](https://vercel.com/get-started.md) was fetched and followed using its Codex route.

| Component | Verified state |
|---|---|
| Node.js | v26.13.0 installed globally through Homebrew |
| Vercel CLI | 65.10.0 installed globally; `vercel whoami` returns `lsantus-mines` |
| Guidance | Official Vercel plugin installed for Codex in user scope via `npx plugins add vercel/vercel-plugin --target codex --scope user --yes`; no duplicate standalone skills installed |
| MCP | User-wide `vercel` server added at exactly `https://mcp.vercel.com`; OAuth completed successfully |
| MCP config | Codex user configuration, `~/.codex/config.toml`; unrelated server entries preserved |
| Authenticated MCP check | `search_vercel_documentation` and `list_teams` not run: new server tools are not exposed in this running session |
| Reload | Plugin installer requests restarting the agent tools to load the new plugin; restart/reload not performed automatically |
| Authenticated CLI check | `vercel teams ls` succeeded: Team Montagne, Hobby; existing project found and inspected |
| Existing production | `deploy-project-product-management` under Team Montagne, deployment Ready; public URL below verified without credentials |

[Public FlowAssist demo](https://deploy-project-product-management.vercel.app). No duplicate Vercel project was created and no temporary accountless deployment was used. HTML/JS/CSS bytes match the v0.3 source; browser rendering remains unverified. The workspace is not locally linked via `.vercel/` because the read-only project checks did not require it.

Cross-repository automation is verified: the [push-triggered run](https://github.com/BenjaminAHS/project-product-management/actions/runs/41667205280) succeeded for primary `e33deb3`. The [secret guide](ACTIVER_SYNC_GITHUB.md) remains the setup/renewal reference. Restart/reload Codex to make the newly installed plugin/MCP tools available for subsequent work; authenticated MCP tool verification remains outstanding until then.
