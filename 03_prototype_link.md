# 03 — Prototype link · FlowAssist

**Version:** v0.3 · 3 November 2026 · S3 surface; Vercel deployment prepared, publication pending; synthetic data only.

- **Link:** [Open the prototype source](prototype/index.html). Download/clone the repository and open `prototype/index.html` in a browser; GitHub's file view shows source rather than executing HTML. No installation, account, API key or server is required.
- **Optional HTTP preview:** from repository root, run `python -m http.server 8000 --bind 127.0.0.1`, then open `http://127.0.0.1:8000/prototype/`. Stop with Ctrl-C.
- **Public hosting:** [Vercel configuration](vercel.json) is ready to serve the prototype at `/`. The primary repository belongs to BenjaminAHS; Vercel’s source copy is [lsantus-mines/deploy-project-product-management](https://github.com/lsantus-mines/deploy-project-product-management), whose v0.3 files have been verified. A primary-push sync workflow is prepared and requires the `DEPLOY_REPO_TOKEN` Actions secret. Vercel publication and anonymous access are not yet confirmed. Follow the [deployment handover](prototype/DEPLOYMENT.md); add the verified production URL here after deployment.
- **Tool:** Codex-assisted HTML/CSS/JavaScript; Sites local-only workflow. Local artifact follows the assignment's repository deliverable; Vercel publication is prepared separately; no production integration is claimed.
- **Time box:** designed as an under-one-hour surface exercise; actual elapsed build time was not instrumented and is not presented as a measurement.
- **Versions:** v0.1 has ready/ambiguous/compliance/access-denied cases, source inspection, review, editor insertion and context handover. v0.2 implements design decisions D01–D05: inspect all sources, plain-language ambiguity, timestamped handover, compliance routing and safe manual mode. v0.3 adds a redesigned responsive workspace, search/filters, review progress, isolated in-tab drafts, keyboard shortcuts, reply copying and explicit replacement confirmation. These are desk-based revisions; no participant iteration is claimed. [Changelog](prototype/CHANGELOG.md).

## The prompt used — the brief in three paragraphs

```text
Paragraph 1 — user and job:
Build a local clickable FlowAssist prototype for Karim, a Tier-1 PayFlow B2B payment operations specialist. Place it in an internal Zendesk-like inbox. He investigates a merchant's missing payment, checks transaction evidence, reviews a cited reply, and either places it in his human editor or escalates. Use fictional tickets and records only. This is a scripted S3 research surface, not a live bank or LLM implementation.

Paragraph 2 — screen and controls:
Show an assigned-ticket list, original message and human reply editor, plus a payment investigation sidebar with verified merchant, transaction, source IDs and timestamps, editable draft and source detail. Require source inspection and explicit review before Use draft in editor. Invalidate review after a draft edit and clear state on ticket selection. Add a handover reason, safe agent note, Escalate with context, Continue manually and Reset test. Show the handover packet locally. Make the page responsive, keyboard usable and explicit that no message is sent.

Paragraph 3 — routing and trust:
Include one grounded tracing example, an ambiguous two-candidate payment, a compliance-hold request and a denied foreign reference. Keep drafts suppressed for blocked cases and show no unauthorized source details. Explain context-only versus human-only in plain language. Retrieval candidates are L3, drafts L2, customer send person-only; no refunds, hold release, ledger writes or autonomous replies. Use synthetic data, no API calls, external assets or persistence. Keep all interactions local and label every simulation.
```

## Test walkthrough (facilitator only)
1. Start at DEMO-01: inspect LED-100 and CLE-100, distinguish sent-to-bank from beneficiary credit, review, insert into editor. Try editing a draft and observe that review resets.
2. Open DEMO-02: two authorized candidates, no draft. Choose “Ambiguous transaction”, optionally add safe notes, escalate and inspect preserved source IDs.
3. DEMO-03 routes compliance to a person. DEMO-04 exposes no transaction evidence. Switching tickets resets inspection/review and restores only the selected ticket’s own text; reset clears all in-tab work and restores DEMO-01.
4. Reproduce T01/T02 from `03_user_research.md` as acceptance scenarios. These do not count as participant usability tests.

## Verification and limits
See [verification report](prototype/verification.md) for reproducible structural and JavaScript interaction checks. The v0.3 source is a scripted interface, without a live model, payment system or Zendesk connection.

No rendered screenshot is attached: the browser execution tool is not exposed in this session. Rendering, responsive layout and keyboard navigation have not been verified in a browser. No model accuracy, participant task time or 41.2% saving has been measured.
