# 03 — User needs and design decisions · FlowAssist

**Updated 9 November 2026.** Three conversations and a prototype test were run on 9 November (section 0). Sections 1–6 are the earlier desk-based synthesis of 3 November; its decisions D01–D05 are team decisions, and D06–D10 come from the conversations and the test.

## 0. Conversations and prototype test · 9 November 2026

### Who we talked to
| # | Profile (no personal data) | Basis of the answers | Relation | Interviewer |
|---|---|---|---|---|
| P1 | Former accounting intern | Past work experience | Friend of the team | Antoine |
| P2 | Former customer-support agent | Past work experience | Friend of the team | Antoine |
| P3 | No direct payments experience | Classmate in role (Tier-1 agent) | Friend of the team | Antoine |

Raw answers, anonymized and word for word: [research/interviews_2026-11-09.csv](research/interviews_2026-11-09.csv).

**Limits.** Most questions were scenarios ("what would you do if…") rather than the Mom Test's "tell me about the last time", so the answers describe intended behaviour, not observed past behaviour. P1 and P2 answered from real jobs; P3 played the role. Three friends of the team are a small, friendly sample.

### What we heard
| Quote (original French) | In English | Who | Brief assumption | Effect |
|---|---|---|---|---|
| « Je lui explique que "envoyé" ne veut pas forcément dire "déjà crédité". » | "Sent" does not necessarily mean "already credited". | P2 | sent_to_bank ≠ credited (D01, policy P03) | Confirms |
| « Être claire et rassurante, sans promettre une date qu'on ne maîtrise pas. » | Clear and reassuring, without promising a date we don't control. | P1 | No ETA or promise (P03) | Confirms |
| « …une estimation du délai si on en a une » · « Je donne le délai habituel » | An estimate of the delay if we have one · I give the usual delay. | P1, P2 | Drafts never mention timing | **Contradicts → D07** |
| « Je lui dis précisément quelle est la prochaine étape et quand il aura de nos nouvelles. » · « je lui donnerais un délai de suivi » | I tell them exactly the next step and when they'll hear from us · I'd give a follow-up time. | P2, P3 | Context-only and handover only explain the block | **New → D06** |
| « …dans un langage normal, pas avec du jargon bancaire. » | In normal language, not banking jargon. | P2 | Status wording mirrors ledger terms | **New → D08** |
| « …je lui demande une référence ou un justificatif, puis je transmets le cas à l'équipe paiements. » | I ask for a reference or proof, then pass the case to the payments team. | P1 | Missing reference → ask, then hand over (D02) | Confirms |
| « Je n'essaierais pas de l'interpréter au hasard. » | I wouldn't guess at a status I don't understand. | P3 | Unknown status → no draft | Confirms |
| « Savoir jusqu'où je peux aller seule… quand escalader. » | Knowing how far I can go alone… when to escalate. | P3 | Visible gate and escalation reason | Confirms |
| « Est-ce qu'il nous a déjà contactés, est-ce qu'il y a d'autres virements concernés ? » | Has he contacted us before, are other transfers involved? | P2 | Account-history panel (v0.4) | Confirms |

### Prototype test
All three tried the hosted prototype on task DEMO-01 ("find what happened to the payment and prepare a reply you would send"). Details were **self-reported after the session** through seven questions, not observed live; raw answers: [research/prototype_test_2026-11-09.csv](research/prototype_test_2026-11-09.csv).

| Tester | Finished without help? | Time | Where they hesitated | What they expected instead | Opened both sources? | Read sent_to_bank as "arrived"? |
|---|---|---|---|---|---|---|
| P1 | Partly | ~8 min | Status "sent to bank": finished, or something left to check? | An explanation of the status and the next step | Yes | **Yes** |
| P2 | Yes | ~5 min | Moving facts from the sources into the draft: had I checked everything? | A short checklist of checks before the reply | Yes | No |
| P3 | No | ~12 min | Which source to open first, how to read ledger vs clearing | The tool saying where to look and what each source confirms | Don't remember | **Yes** |

**Result:** 1 of 3 finished without help. **2 of 3 read "sent to bank" as money already received**, which is the misreading D01 guards against and the strongest evidence for D08. Requested changes: plain status words (P1, P3), a summary of verified facts above the draft (P2), guidance on which source confirms what (P3).

### Desirability gate
- [ ] Testers finished the task without help (1 of 3; P1 partly, P3 not)
- [ ] They told us what they did last time (partly: P1 and P2 drew on past jobs, through scenario questions)
- [ ] At least one said "I want this before…" (not asked)
- [x] Our out-of-scope list grew; our success criterion did not move (D06–D10 refine wording and guidance; the 41.2% criterion is unchanged)

### Decisions from the conversations
| ID | Change for v2 | Evidence | Where | Status |
|---|---|---|---|---|
| D06 | Every context-only or handover reply states the next step and when the merchant will hear back | P2, P3 | Brief §9, spec | Brief and spec updated; prototype unchanged |
| D07 | A draft may state a *documented* typical processing time for the rail, labelled "typical, not guaranteed"; never a date for this payment | P1, P2 (P1 also: no promised date) | Brief §9–10, spec | Pending Ops/Legal approval; not in prototype |
| D08 | Status wording in plain language (e.g. "sent to the recipient's bank, not yet confirmed as received") instead of ledger terms | P2 interview; test: P1 and P3 read sent_to_bank as received | Brief §9, spec | Brief and spec updated; prototype unchanged |
| D09 | A "verified facts" summary above the draft (transaction, amount, status, event time, sources checked), as a pre-insert checklist | Test: P2 | Brief §9, spec | Brief and spec updated; prototype unchanged |
| D10 | Source guidance: what the ledger record and the clearing record each confirm, and which to open first | Test: P3 (and P1 asking for the next step) | Brief §9, spec | Brief and spec updated; prototype unchanged |

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
**User-driven changes: D06–D10** (section 0), from the 9 November conversations and prototype test. D01–D05 remain team design decisions. The [original brief](research/brief_v1.md) is retained for comparison.

Users could not settle whether a typical processing time reassures or risks reading as a promise (P1 wants both an estimate and no promised date): Ops and Legal decide D07. Users cannot determine the economic hurdle (CFO/Product), measured savings and quality (paired timing and independent graders), model choice (Engineering evaluation), legal basis and retention (DPO/Legal), or scope approval (Ops/CCO). The 41.2% threshold remains fixed.

## 6. Decision
**Proceed under a conditional design GO.** Three conversations with friends of the team support the safety rules (sent ≠ credited, no promised date, ask for a reference, escalate when unsure) and add D06–D10. The test found a real usability problem: 2 of 3 testers read "sent to bank" as received, and only 1 of 3 finished alone. Desirability is not validated: the sample is small and friendly, questions were mostly hypothetical, and test details were self-reported. Technical, economic and production gates remain separate.
