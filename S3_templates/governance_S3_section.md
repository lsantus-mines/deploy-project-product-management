## Session 3 — data and trust level
> Paste this section into your governance.md (it replaces “Session 3 — data (to come)”).

### The six-question data audit
| # | Question | Our answer | Source type (measured / analogy / guess) | To check with |
|---|---|---|---|---|
| 1 | **Provenance** — where does each row come from, who collected it, when? | | | |
| 2 | **Volume & labels** — how many rows, labelled by whom, with which guideline? | | | |
| 3 | **Coverage** — which languages, plans, regions vs the users we ship to? | | | |
| 4 | **Rights** — legal basis (GDPR art. 6), what the customer contract allows, retention | | | DPO |
| 5 | **Leakage** — can a row reappear in the test set, or in another customer's answer? | | | |
| 6 | **Freshness** — how old is it, does that world still exist? | | | |

- **Purpose limitation (GDPR art. 5):** what we use the data for, and for how long we keep it: …
- **Isolation between customers:** how the retrieval index prevents customer A's data from appearing in customer B's answer: …
- **Known gaps by segment** (language, plan, region): …

### Trust level per step (same scale as Session 1)
| Step | L1 suggests · L2 drafts, a person approves · L3 acts on a scope, a person samples · L4 acts alone under a threshold · or person only | Why (cost of an error) |
|---|---|---|
| | | |
