# S3 v0.3 verification · 3 November 2026

Run from the repository root on macOS:

```sh
python scripts/verify_s3.py
```

The dependency-free checker uses the system JavaScriptCore engine and a minimal DOM initialized from HTML attributes. It verifies the 20 CSV fixtures and seven proposed eligible labels, design-review register, policy references, document links, HTML/JavaScript IDs, stylesheet inclusion, Vercel asset configuration and shared brief/annex criterion.

**44 passing interaction assertions** cover both-source inspection, approval, edit invalidation, manual fallback/resume, ticket switching, per-ticket/per-merchant text isolation, restored text without restored approval, replacement confirmation/cancellation, ambiguity, required handover reason/note, timestamped authorized sources, compliance routing, denied data, note/reason preview invalidation, reset, search/filter/empty states and keyboard dispatch outside text fields. Untrusted notes are inserted as text rather than HTML.

Additional packaging checks passed: HTML tags are correctly nested; the deployment output contains byte-identical copies of `index.html`, `app.js` and `styles.css`. No runtime dependencies or external asset requests are introduced.

These checks do not render the page or use a real clipboard. Clipboard behavior has a manual-selection fallback but has not been verified in a browser. Responsive layout, focus visibility, keyboard navigation, actual clipboard permission behavior and screenshot capture remain unverified because the browser execution tool is unavailable in this session. No backend security, model performance, user validation or productivity result is implied.

## Public deployment verification
On 3 November 2026, the [production URL](https://deploy-project-product-management.vercel.app) returned HTTP 200 without credentials or a redirect to login. Downloaded `index.html`, `app.js` and `styles.css` are byte-identical to the v0.3 local files. Vercel reports production deployment `dpl_BAsGPzfr7U3MKJpN75L4dH9W62NM` as Ready under Team Montagne. This is HTTP/asset verification, not rendered browser or participant testing.
