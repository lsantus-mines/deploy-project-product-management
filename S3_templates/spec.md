# spec.md — executable spec · [agent name] · skeleton v0

> Session 3 skeleton, completed in Session 4. This is what Claude Code (or Cursor) reads to build the prototype.
> Same content as 03_product_brief.md, but nothing can stay vague: inputs, outputs, edge cases, fallbacks, done.

## problem
One paragraph — from 03_product_brief.md §1.

## user_workflow
Steps with inputs and outputs, and the trust level of each step.
```
- read      : ticket text + account plan   -> category, confidence      (L4 above threshold)
- retrieve  : category + text               -> top-3 KB passages          (L3)
- draft     : passages + text               -> reply with citations       (L2 — a person approves)
- check     : reply                         -> policy pass | block        (L2)
- send      : reply                         -> customer                   (person only)
```

## io_contracts
```
ticket : {id, text, plan, language}
draft  : {text, citations[{kb_id, span}], confidence, policy: pass|block}
```

## edge_cases
- no KB passage found → …
- language not covered → …
- personal data in the ticket → …
- out-of-scope category (e.g. payroll, billing) → …

## fallbacks
- confidence below [0.7] → escalate to a person, with the context
- policy block → show the reason to the agent, no draft

## done_criteria
- the success criterion from 03_product_brief.md §7 (e.g. ≥ 45 % of drafts sendable without edit on the eval-set)
- zero policy breaches on the adversarial tickets

## out_of_scope
The WON'T column of the MoSCoW board.

## eval_set
`evals/tickets_v0.csv` — 20 tickets now, growing to 200 by Session 5.
