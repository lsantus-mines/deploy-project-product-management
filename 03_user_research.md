# 03 — User needs and design decisions · FlowAssist

**3 November 2026 · Desk-based design synthesis.** No participant interviews or usability sessions were conducted. This document completes the needs analysis and v2 decision record without attributing decisions to users. It does not satisfy the assignment’s requirement for three real conversations and two participant tests.

## 1. Target users and concrete work situations
| Profile | Situation to support | Need | Design response |
|---|---|---|---|
| Tier-1 payment specialist (Karim) | A supplier has not received a payment marked sent to bank | Separate the bank transmission event from confirmed beneficiary credit | Display status and event time beside sources; preserve uncertainty in the reply |
| Tier-1 covering a colleague’s queue | Two €500 payments have the same date and no unique reference | Avoid choosing a transaction from amount alone | Suppress draft; explain missing reference; retain both authorized candidate IDs |
| Tier-2 payments / compliance specialist | A blocked request arrives after several manual searches | Understand what is known, what is missing and why it was escalated | Handover includes verified merchant, gate, reason, authorized sources and timestamps; sensitive requests name the compliance destination |

These profiles are product scenarios derived from S1/S2 and the existing fixtures, not recruited participants. Frequency and reported pain have not been measured.

## 2. Design findings and decisions
| ID | Design finding | Basis | Decision for v2 | Acceptance check |
|---|---|---|---|---|
| D01 | One opened ledger record does not establish the clearing event | DEMO-01 has distinct LED-100 and CLE-100 evidence | Require inspection of every displayed source plus explicit review before editor insertion | Opening only one source leaves insertion disabled |
| D02 | “Context only” does not tell the operator what to do next | DEMO-02 has two authorized €500 candidates | Lead with “A unique payment reference is needed”; explain that no candidate can be selected safely | Ambiguous ticket has no draft and names reference request/escalation |
| D03 | A source ID without a retrieval timestamp makes freshness hard to inspect | Spec requires source freshness and preserved handover context | Show fixed snapshot retrieval time in every evidence record and handover packet | Packet retains authorized IDs and snapshot times |
| D04 | A compliance hold requires a different receiving specialist | Compliance requests are explicitly outside tracing scope | Route the sensitive scenario to Tier-2 compliance; other tickets to Tier-2 payments | Packet destination matches scenario |
| D05 | Continuing manually should end the current draft approval path | Manual handling is the fallback at every step | Disable draft insertion after manual handling until ticket reset/reselection | Source/review interactions cannot re-enable insertion in manual mode |

## 3. v1 → v2 decision log
| Brief section | v1 | v2 | Trace |
|---|---|---|---|
| §6 integration | Inspect a source and approve | Inspect every source, approve; edits invalidate review; manual mode disables insertion | D01, D05 |
| §2 fallback | Generic context-only wording | Missing reference explained as the next required action | D02 |
| §6 handover | Source IDs and generic Tier-2 destination | Snapshot timestamps and payments/compliance destination | D03, D04 |
| §3 scope | Three MUST, five WON’T | Same scope; refinements fit inside safe gate, cited draft and handover | D01–D05 |

## 4. Two reproducible task scenarios
These are acceptance scenarios, not completed participant tests. No task time, success percentage, hesitation, satisfaction or urgent demand is claimed.

**T01 — Grounded tracing reply.** Open DEMO-01. Inspect LED-100 only: insertion remains disabled. Inspect CLE-100, read that beneficiary credit is not confirmed, and explicitly review. Insert the draft; the editor contains the cited reply and no message is sent. Edit the draft: review resets. Switch tickets: inspection and approval reset; an unvisited ticket has an empty editor, while revisiting restores only its own text. An existing different reply requires explicit replacement confirmation.

**T02 — Ambiguity and specialist handover.** Open DEMO-02. Confirm that a unique reference is needed and no draft is available. Choose “Ambiguous transaction”, add safe context and escalate. The preview names Tier-2 payments, the merchant, reason, both authorized sources and their snapshot times. Open DEMO-03 and use the sensitive-request reason: destination is Tier-2 compliance. DEMO-04 has no transaction sources or foreign owner details.

## 5. What the users changed / could not decide
**User-driven changes: none established.** D01–D05 are team design decisions. They improve the v2 surface but do not establish desirability. The [original brief](research/brief_v1.md) is retained for comparison.

Users cannot determine the economic hurdle (CFO/Product), measured savings and quality (paired timing and independent graders), model choice (Engineering evaluation), legal basis and retention (DPO/Legal), or scope approval (Ops/CCO). The 41.2% threshold remains fixed.

## 6. Decision
**Proceed with the S4 implementation under a conditional design GO.** Desirability is unvalidated. Technical, economic and production gates remain separate; no enthusiasm, completed interview or human label approval is asserted. Participant research is excluded by the team’s current decision, so its assignment requirement remains unmet.
