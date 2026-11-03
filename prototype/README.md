# FlowAssist · S3 workspace v0.3

[Open the public demo](https://deploy-project-product-management.vercel.app) or open `index.html` in a browser, keeping `app.js` and `styles.css` beside it. No dependency installation, external fonts, API keys or account is needed. Launch instructions, design prompt and scope: [prototype record](../03_prototype_link.md).

The interface provides a searchable, filterable inbox; merchant request and source-backed payment summary; source inspection and review progress; editable cited suggestion; reply editor with character count and copy action; and timestamped specialist handover. Blocked tickets open the handover panel directly. All four tickets and payment records are synthetic; there is no live LLM, Zendesk or bank connection.

Drafts, manual edits, handover notes and manual mode are retained **per ticket in tab memory**. Switching tickets resets source inspection/approval and displays only that ticket’s own text. Reloading or Reset demo clears all work. A source or approval from another ticket can never authorize insertion. Resuming assisted mode requires source inspection again. Inserting over an existing different reply requires an explicit replacement choice. Editing handover notes/reason invalidates the old preview.

“Use draft” fills the local editor. “Copy reply” copies only the editor contents; if clipboard access fails, the editor selects the text for manual copying. “Prepare handover” displays a local preview. Nothing sends a message, modifies a transaction or contacts a queue.

Keyboard: `/` focuses search; `J` / `K` select the next/previous visible ticket outside form fields; `Alt+Enter` uses an already reviewed draft; `Escape` closes help or leaves search. The keyboard help button lists these shortcuts. Small screens follow message → investigation → summary → reply in the same DOM order used by keyboard navigation.

Checks: run `python scripts/verify_s3.py` on macOS. See [verification report](verification.md), [changelog](CHANGELOG.md) and [acceptance scenarios](../03_user_research.md). Browser rendering, keyboard behavior in an actual browser and mobile appearance remain unverified in this environment.

Vercel: [root configuration](../vercel.json) copies `index.html`, `app.js` and `styles.css` into `dist/`, serving at `/`. Vercel’s source copy is `lsantus-mines/deploy-project-product-management`; product development stays in `BenjaminAHS/project-product-management`. The primary-push sync workflow requires its destination-write secret before automated runs can succeed. See [deployment guide](DEPLOYMENT.md); the production URL is verified above (anonymous HTTP 200 and matching HTML/JS/CSS).
