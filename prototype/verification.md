# FlowAssist v0.4 verification · 3 November 2026

```sh
python scripts/verify_s3.py
```

Requires Python and Node.js, without third-party test packages. Artifact checks retain the S3 CSV/label-review/policy/link/criterion checks, verify HTML IDs and the five-asset Vercel configuration, then run `node --test scripts/test_app.cjs`.

**32 passing scenarios** test the actual domain engine and UI handlers. Domain checks cover all ten routes; merchant isolation; reference-only matching; currency/precision/freshness/schema/conflict rejection; net/gross reconciliation; regulatory/fund-action/injection/secret routes; EN/FR/DE generation; generated/edited draft evaluation; and safe handover. Interaction checks cover every-source review, editor replacement, ticket/merchant buffer isolation, manual fallback/resumption, final human approval, closure/reopening, awaiting-reference resolution, specialist transfer, new cases, search/filter/keyboard dispatch, session restoration, corrupted storage, sanitized persistence, scoped exports and stopped/paused handling timers.

The UI harness provides a minimal DOM initialized from the HTML. It executes `data.js`, `engine.js` and `app.js` in a Node VM. It does not render CSS, run a real clipboard/download, or prove real focus/accessibility/mobile behavior. Separate HTML-nesting and build-asset checks have passed. Browser rendering and screenshots remain unverified because the browser execution tool is unavailable in this session.

The earlier v0.3 publication returned anonymous HTTP 200 with matching HTML/JS/CSS under Team Montagne. The v0.4 release uses the same public URL; the release handover records its current production verification separately. [Public application](https://deploy-project-product-management.vercel.app).

No test result establishes live backend isolation, regulatory compliance, model-grounding accuracy, user desirability, QA ≥92%, a paired AHT saving or the 41.2% hurdle. The local journal is editable browser data. The model-based evaluator and agent-level A/B from P2 remain target integrations/evaluation work.

## Verified v0.4 release
Production deployment `dpl_4isLr4HL3Y1s1a3DgVSzm6rgf61g` is Ready. On 3 November 2026, anonymous HTTP checks confirmed byte-identical `index.html`, `styles.css`, `data.js`, `engine.js` and `app.js` against source `e33deb3`. Run `python scripts/verify_production.py` to repeat. The [primary-push synchronization workflow](https://github.com/BenjaminAHS/project-product-management/actions/runs/41667205280) completed successfully for that source commit. Browser rendering, real external integrations and model quality remain outside this verification.

## Session 4 · 9 November 2026

`python3 scripts/verify_s4.py` validates the 50-case development suite and both pinned baseline/current runs. All 50 current states agree, with 15 drafts. Confidence is validated for model-derived match inputs; it never overrides merchant scope or source checks. The unmodified Paylio starter was run with the existing Anaconda environment (`scripts/run_paylio.py`); evidence is in `docs/evidence/s4/paylio-run.txt`. Browser verification was attempted but no in-app execution tool or runnable local Playwright package is available in this environment.
