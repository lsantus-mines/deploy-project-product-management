# Fieldwork kit — 3 conversations + 2 think-aloud tests · FlowAssist

**Purpose:** close the Assignment 3 gap (also required by the Assignment 4 checklist: "brief v2 after three conversations"). Fill this file **by hand, from real sessions**. Assignment 3 forbids AI-invented research: every quote and observation must come from a person you spoke to. Classmates in role are allowed **if said explicitly** in the table.

**When done:** paste §1, §3, §5 and §6 at the top of `03_user_research.md` (keep the existing desk synthesis below them as "Design decisions D01–D05"), then rewrite brief §9–§10 from §6. Each person who ran a session commits their own notes with their own Git account.

**Time budget:** 3 × 20 min conversations + 2 × 10 min tests (done right after conversations 1 and 2) ≈ 1 h 20 of fieldwork, plus 30 min synthesis.

---

## 0. Who to recruit (pick three, record which kind)

| Profile, best to acceptable | Why it fits FlowAssist |
|---|---|
| Someone who works or worked in support, payment operations, finance ops or accounts payable/receivable (internship, part-time job, family member) | The real Tier-1 user: has traced a payment from a ticket |
| Someone who has chased a late B2B or marketplace payout as a supplier, seller or freelancer | The merchant side: knows what a useful reply looks like |
| A classmate briefed as **Karim, Tier-1 payment specialist at PayFlow B2B** (give them the brief §1 paragraph, nothing more) | Allowed, must be labelled "classmate in role". Weakest evidence |

Never record personal data: role and company type only.

## 1. Who we talked to

| # | Who (role, company type — no personal data) | Real user or classmate in role? | Date | Interviewer · note-taker | Also did the prototype test? |
|---|---|---|---|---|---|
| 1 | | | | | yes / no |
| 2 | | | | | yes / no |
| 3 | | | | | yes / no |

## 2. Interview guide — 20 min, past behaviour only

Interviewer asks; note-taker writes **their words**, not your interpretation. Never show or describe FlowAssist before the conversation ends.

**Opening (2 min)**
- "We're students studying how people handle payment questions at work. No product to sell. Can you tell us about your role?"

**The last time (8 min)** — anchor everything on one real event
1. Tell me about the last time someone asked you where a payment was (or you asked a company where your payment was). What happened, step by step?
2. Which screens, tools or people did you check, in what order? How long did it take in total?
3. How did you know you had found the *right* transaction? What made you sure, or not sure?
4. What did you finally tell the person? Did you have to correct it later?

**Where it hurts (6 min)**
5. What was the slowest or most annoying part of that time?
6. Has it gone wrong before — wrong transaction, wrong status, wrong customer's data? What happened next and who fixed it?
7. When you couldn't answer, who did you hand it to? What did you have to re-explain?
8. What have you already tried to make this faster (templates, saved searches, asking a colleague)? What did that cost you?

**Close (4 min)**
9. Is there anything about that time I should have asked and didn't?
10. Who else does this often whom we could talk to?

**Never ask:** "Would you use an AI that…?" · "Do you like this idea?" · "How much would you pay?" · "Wouldn't it be great if…?"
**If they speculate** ("I would probably…"), steer back: "What did you do the last time?"

### Notes — conversation 1
- Last event, step by step:
- Tools / people checked, minutes:
- How they confirmed the right transaction:
- What went wrong / handover:
- Workarounds already tried:
- Verbatim quotes (in quotes, word for word):

### Notes — conversation 2
- Last event, step by step:
- Tools / people checked, minutes:
- How they confirmed the right transaction:
- What went wrong / handover:
- Workarounds already tried:
- Verbatim quotes:

### Notes — conversation 3
- Last event, step by step:
- Tools / people checked, minutes:
- How they confirmed the right transaction:
- What went wrong / handover:
- Workarounds already tried:
- Verbatim quotes:

## 3. What we heard (facts, in their words)

Link each fact to the brief or canvas assumption it touches. "Contradicts" rows are the most valuable: they are what v2 must change.

| # | Quote or observed behaviour (source: conv. 1/2/3) | Brief / canvas assumption touched | Confirms · contradicts · new |
|---|---|---|---|
| H1 | | e.g. "pain sits in finding the transaction" (design §2) | |
| H2 | | e.g. "amount + date is not enough to pick a transaction" (D02) | |
| H3 | | e.g. "Tier-2 needs source IDs and timestamps in the handover" (D03) | |
| H4 | | e.g. ~6 min per tracing ticket (S2 guess) | |
| H5 | | | |

## 4. Think-aloud test protocol — 10 min, two of the three people

**Setup:** open <https://deploy-project-product-management.vercel.app> on your laptop, click **Reset test** so the session starts clean. Start a phone timer. Note-taker sits beside them, silent.

**Script to read aloud (do not improvise):**
> "This is a rough prototype of a tool for a payments support agent. We're testing the prototype, not you. Please say out loud what you're looking at and thinking. I can't help or answer questions while you work. Here's the task:"

**The task (same for both testers):**
> "A merchant writes: *'Where is my payment?'* (ticket DEMO-01). Find out what happened to the payment and prepare a reply you'd be comfortable sending. You don't actually send anything. Tell me when you're done."

**Rules:** don't help. If they're stuck for 60 s, say only "What would you do next?" and record it as *needed help*. Stop at 8 min.

**Optional second task, if time allows:** ticket DEMO-02 ("Two possible payments"). This tests whether they understand why no draft is offered.

**Note-taker writes down:** where the cursor hesitates, everything they say, whether they open **all** sources before inserting the draft (D01), and whether they notice the difference between "sent to bank" and "credited".

## 5. Usability test results

**Prototype link:** see `03_prototype_link.md` · **Task given:** DEMO-01 "Where is my payment?", prepare a reply you'd send

| Tester (# from §1) | Finished without help? (yes / no) | Time (min:s) | Where they hesitated | What they expected instead | Quote |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

### Desirability gate
- [ ] 2 of 2 finished the task without help
- [ ] They told us what they did last time, not what they would do
- [ ] At least one said something like "I want this before…"
- [ ] Our out-of-scope list grew; our success criterion did not move

**Decision:** go to Session 5 · or back to the brief — because …

## 6. What the users changed → brief v2 §9

Only changes backed by evidence from §3 or §5. If nobody changed anything, write that. It is an honest result.

| Change in brief v2 / prototype | Evidence (H# or tester + quote) | Brief section edited |
|---|---|---|
| | | |
| | | |

## 7. What they could not decide → brief v2 §10

Questions users could not answer, or disagreed on, and who in the company owns them (CFO, CCO/Ops, DPO, Engineering…).

| Open question | What each person said | Owner |
|---|---|---|
| | | |
