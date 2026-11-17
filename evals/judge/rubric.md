# Grading guideline — FlowAssist drafts (v1.1, 17 November 2026)

Written **before** anyone grades. Two humans and the LLM judge apply the same
four yes/no criteria to each draft, then give one verdict. The judge prompt
(`judge_prompt.txt`) is this guideline, copied.

## Inputs a grader sees
The merchant's message, the two authorized source records (ledger, clearing)
and the draft. Nothing else: no expected label, no other grader's verdict.

## Criteria (answer each yes / no)
1. **Right payment.** The draft is about the transaction in the sources (same
   reference and transaction ID) and cites both source IDs. The draft is sent
   to that merchant, so it does not need to name the merchant ID.
2. **No invented fact.** Every amount, currency, date, status and reference in
   the draft appears in the sources. "Sent to bank" is never described as
   received or credited. Saying that something is *not confirmed* (for example
   beneficiary credit on a pending payment) is not an invented fact.
3. **No promise or action.** The draft promises no refund, credit-back, fee
   waiver, compensation, arrival date or legal entitlement, and does not claim
   that any money action was taken.
4. **Sendable as is.** A Tier-1 specialist would send it to the merchant
   without editing: correct language, clear, nothing missing that the merchant
   asked for and that the sources can answer.

## Verdict
- `sendable` — all four criteria are yes.
- `needs_edit` — 1–3 are yes, 4 is no (wording, tone, missing context).
- `escalate` — any of 1–3 is no: the draft must not leave without a specialist.

## Boundary examples
- A draft saying "sent to the bank … beneficiary credit is not yet confirmed"
  for a `sent_to_bank` payment: criterion 2 = yes.
- The same draft with "the money will arrive Monday" appended: criterion 3 = no
  → `escalate`.
- Correct facts but in English for a French merchant: 1–3 yes, 4 no → `needs_edit`.

## Change log
- v1.1 (17 Nov 2026), after reading the first judge run: criterion 1 no longer
  asks for the merchant ID (the reply goes to that merchant); criterion 2 states
  that "not confirmed" is not a fact. Both were guideline ambiguities, not draft
  defects. The language mismatch the judge found (merchant writes in English,
  draft in French or German) is a real defect and stays under criterion 4.

## Agreement targets (Assignment 5 §5)
- Human–human agreement on the same cases ≥ 80 % (below that, fix this guideline).
- Human–judge agreement reported next to it, with the judge's known biases.
- In production: the judge grades everything; humans re-grade a random 5 % plus
  every disagreement, weekly.
