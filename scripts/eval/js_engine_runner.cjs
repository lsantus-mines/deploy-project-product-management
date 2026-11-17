/* Run prototype/engine.js on cases read from stdin; used by tests/test_parity.py.
   Input: [{data, ticket, reference, texts:[...]}]. Output: one summary per case. */
"use strict";
const path = require("node:path");
require(path.join(__dirname, "..", "..", "prototype/engine.js"));
const E = globalThis.FlowEngine;
const cases = JSON.parse(require("node:fs").readFileSync(0, "utf8"));
const out = cases.map((c) => {
  const a = E.analyze(c.ticket, c.data, c.reference || "");
  return {
    state: a.state,
    gate: a.gate,
    intent: a.intent,
    queue: a.queue,
    reason: a.reason,
    draft: a.draft,
    transaction: a.transaction ? a.transaction.id : null,
    sources: a.sources.map((s) => [s.id, s.text]),
    candidates: a.candidates.map((t) => t.id),
    checks: a.checks,
    evaluations: (c.texts || []).map((t) => {
      const r = E.evaluateDraft(a, t);
      return { passed: r.passed, critical: r.critical, issues: r.issues };
    }),
  };
});
process.stdout.write(JSON.stringify(out));
