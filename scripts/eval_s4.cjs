/* Development evaluation, never a substitute for independent human grading. */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const baseline = process.argv.includes('--baseline');
const enginePath = baseline ? 'evals/engine_baseline_v0.js' : 'prototype/engine.js';
require(path.join(root, enginePath));
const fixturePath = baseline ? 'evals/fixtures_baseline_v0.json' : 'evals/fixtures_v0.json';
const fixtures = JSON.parse(fs.readFileSync(path.join(root, fixturePath)));
if (fixtures.length !== 50 || new Set(fixtures.map(f => f.id)).size !== 50) throw Error('Expected 50 unique fixtures');
const results = fixtures.map(f => {
  const a = FlowEngine.analyze(f.ticket, f.data);
  const check = a.draft ? FlowEngine.evaluateDraft(a, a.draft) : null;
  return {id:f.id, expected:f.expectedState, actual:a.state, pass:a.state===f.expectedState,
    draft:a.draft, policyPass:check?.passed ?? false, gate:a.gate,
    sourceIds:a.sources.map(s=>s.id), transaction:a.transaction?.id ?? null,
    foreignSources:a.sources.filter(s=>s.merchant!==f.ticket.merchant).length,
    unsupportedContract:f.unsupportedContract};
});
const hash = p => crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex');
const output = {kind:'deterministic development run; human sendability ungraded',
  engineSHA256:hash(enginePath), fixtureSHA256:hash(fixturePath),
  summary:{cases:results.length,stateMatches:results.filter(r=>r.pass).length,
    drafts:results.filter(r=>r.draft&&r.policyPass).length,
    humanOnlyDrafts:results.filter(r=>r.expected==='human_only'&&r.draft).length,
    foreignSources:results.reduce((n,r)=>n+r.foreignSources,0)},results};
fs.writeFileSync(path.join(root,baseline ? 'evals/results_baseline_v0.json' : 'evals/results_v0.json'),JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify(output.summary,null,2));
for(const r of results.filter(r=>!r.pass)) console.log(r.id,r.expected,'->',r.actual,r.gate);
