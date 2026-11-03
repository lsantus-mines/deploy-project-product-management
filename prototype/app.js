'use strict';
const examples = {
  ready: {id:'DEMO-01', merchant:'M-ALPHA', language:'EN', title:'Where is my payment?', message:'Could you trace our EUR 1,240 payment, reference INV-DEMO? Our supplier is still waiting.', state:'ready', gate:'Unique reference · TX-100 · tenant verified', sources:[{id:'LED-100',text:'M-ALPHA · TX-100 · INV-DEMO\nEUR 1,240 · sent_to_bank\nFetched: 2 Nov 2026, 10:00 UTC'}, {id:'CLE-100',text:'M-ALPHA · TX-100\nSent to bank: 2 Nov 2026, 09:58 UTC\nBeneficiary credit: NOT confirmed\nFetched: 2 Nov 2026, 10:00 UTC'}], draft:'Your EUR 1,240 payment (INV-DEMO, TX-100) was sent to the bank on 2 November at 09:58 UTC. Beneficiary credit is not yet confirmed in the available clearing record. [LED-100; CLE-100]'},
  ambiguous: {id:'DEMO-02', merchant:'M-ALPHA', language:'FR', title:'Two possible payments', message:'Où est notre paiement de 500 euros envoyé hier ? Je ne retrouve pas la référence.', state:'blocked', gate:'A unique payment reference is needed', reason:'Two authorized payments match this amount. Ask for a unique reference or escalate. No draft can be prepared from an arbitrary match.', sources:[{id:'LED-201',text:'M-ALPHA · TX-201 · EUR 500\n1 Nov 2026 · reference INV-A · pending\nFetched: 2 Nov 2026, 10:00 UTC'}, {id:'LED-202',text:'M-ALPHA · TX-202 · EUR 500\n1 Nov 2026 · reference INV-B · pending\nFetched: 2 Nov 2026, 10:00 UTC'}]},
  sensitive: {id:'DEMO-03', merchant:'M-BETA', language:'DE', title:'Release the compliance hold', message:'Unsere Auszahlung ist wegen einer Compliance-Prüfung gesperrt. Bitte erklären Sie den Grund und geben Sie sie frei.', state:'blocked', gate:'Human only · compliance specialist', reason:'Compliance explanations and hold release are outside this MVP. Route to an authorized specialist. No hold diagnosis, release promise or draft is available.', sources:[]},
  denied: {id:'DEMO-04', merchant:'M-ALPHA', language:'EN', title:'Reference outside account', message:'Please show the bank details and current status for TX-FOREIGN.', state:'blocked', gate:'Access denied · no authorized evidence', reason:'The requested reference is unavailable in this assigned merchant scope. No transaction context is exposed. Continue with authorized support or escalate.', sources:[]}
};
const $ = id => document.getElementById(id);
const snapshotTime = '2026-11-02T10:00:00Z';
const ticketButtons = Array.from(document.querySelectorAll('[data-ticket]'));
const buffers = new Map();
let current = 'ready';
let initialized = false;
let inspectedSources = new Set();
let manualMode = false;
let activeFilter = 'all';

function announce(message) {
  $('status').textContent = message;
}

function saveTicket() {
  if (!initialized) return;
  const buffer = {
    draft: $('draft').value,
    editor: $('editor').value,
    note: $('manual-note').value,
    reason: $('reason').value,
    manual: manualMode
  };
  buffers.set(current, buffer);
  $(`saved-${current}`).hidden = !(buffer.editor.trim() || buffer.note.trim() || buffer.draft !== (examples[current].draft || ''));
}

function updateEditor() {
  const text = $('editor').value;
  $('editor-count').textContent = `${text.length.toLocaleString('en')} characters`;
  $('editor-state').textContent = text.trim() ? 'Draft · not sent' : 'Not prepared';
  $('copy-reply').disabled = !text.trim();
}

function hideReplacement() {
  $('replace-confirm').hidden = true;
}

function updateApproval() {
  const t = examples[current];
  const allInspected = t.sources.length > 0 && t.sources.every(s => inspectedSources.has(s.id));
  const approved = allInspected && $('review').checked;
  $('use-draft').disabled = !(t.state === 'ready' && !manualMode && approved && $('draft').value.trim());
  $('review-progress').textContent = manualMode
    ? 'Assisted drafting paused. Resume when you are ready to inspect the sources again.'
    : !allInspected
      ? `${inspectedSources.size}/${t.sources.length} sources inspected. Check every record before using this draft.`
      : !$('review').checked
        ? 'All sources inspected. Check the reply and confirm your review.'
        : 'Reviewed and ready. This places the draft in your editor; it does not send it.';
  const step = approved ? 'step-reply' : allInspected ? 'step-review' : 'step-evidence';
  const order = ['step-evidence', 'step-review', 'step-reply'];
  order.forEach((id, index) => {
    $(id).setAttribute('aria-current', id === step ? 'step' : 'false');
    $(id).classList.toggle('complete', index < order.indexOf(step));
  });
}

function render(key) {
  if (!Object.prototype.hasOwnProperty.call(examples, key)) return;
  saveTicket();
  current = key;
  inspectedSources = new Set();
  const t = examples[key];
  const buffer = buffers.get(key);
  manualMode = Boolean(buffer && buffer.manual);
  ticketButtons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.ticket === key)));
  document.title = `${t.id} · FlowAssist`;
  $('ticket-meta').textContent = `${t.id} · ${t.language}`;
  $('ticket-title').textContent = t.title;
  $('merchant').textContent = `Verified merchant scope · ${t.merchant}`;
  $('message').textContent = t.message;
  $('message-language').textContent = {EN:'English', FR:'Français', DE:'Deutsch'}[t.language] || t.language;
  $('sender-name').textContent = `${t.merchant === 'M-BETA' ? 'Beta' : 'Alpha'} finance team`;
  $('sender-avatar').textContent = t.merchant === 'M-BETA' ? 'B' : 'A';
  $('gate').textContent = t.gate;
  $('gate').className = t.state === 'ready' ? 'safe' : key === 'denied' ? 'safe gate-denied' : 'safe gate-warning';
  $('summary-panel').hidden = key !== 'ready';
  $('payment-amount').textContent = 'EUR 1,240.00';
  $('payment-status').textContent = 'Sent to bank';
  $('payment-status').className = 'ticket-label ready-label';
  $('payment-reference').textContent = 'TX-100';
  $('invoice-reference').textContent = 'INV-DEMO';
  $('source-count').textContent = `${t.sources.length} records`;
  $('sources').replaceChildren();
  t.sources.forEach(s => {
    const button = document.createElement('button');
    button.textContent = `Open ${s.id} · ${s.id.startsWith('CLE') ? 'Clearing event' : 'Ledger record'}`;
    button.setAttribute('aria-controls', 'source-detail');
    button.setAttribute('aria-expanded', 'false');
    button.addEventListener('click', () => {
      $('source-detail').hidden = false;
      $('source-detail').textContent = `${s.id} · ${t.merchant}\n\n${s.text}`;
      inspectedSources.add(s.id);
      Array.from($('sources').children).forEach(b => b.setAttribute('aria-expanded', 'false'));
      button.setAttribute('aria-expanded', 'true');
      button.classList.add('inspected');
      button.textContent = `✓ ${s.id} · ${s.id.startsWith('CLE') ? 'Clearing event' : 'Ledger record'} · inspected`;
      updateApproval();
    });
    $('sources').append(button);
  });
  if (!t.sources.length) {
    const empty = document.createElement('p');
    empty.textContent = 'No authorized evidence available in this scope.';
    empty.className = 'empty';
    $('sources').append(empty);
  }
  $('source-detail').hidden = true;
  $('source-detail').textContent = '';
  $('draft-panel').hidden = t.state !== 'ready' || manualMode;
  $('draft').value = buffer ? buffer.draft : t.draft || '';
  $('blocked').hidden = t.state === 'ready';
  $('blocked').textContent = t.reason || '';
  $('review').checked = false;
  $('editor').value = buffer ? buffer.editor : '';
  $('manual-note').value = buffer ? buffer.note : '';
  $('reason').value = buffer ? buffer.reason : '';
  $('manual-state').hidden = !manualMode;
  $('manual').hidden = manualMode;
  $('handover').open = t.state !== 'ready';
  $('handover-destination').textContent = `Prepare context for ${key === 'sensitive' ? 'Tier-2 compliance' : 'Tier-2 payments'}. Nothing is sent to a real queue.`;
  $('packet').hidden = true;
  $('packet').replaceChildren();
  hideReplacement();
  announce(buffer && (buffer.editor || buffer.note) ? 'Your work on this ticket was restored. Inspect the sources again before using a suggested reply.' : '');
  initialized = true;
  updateEditor();
  updateApproval();
}

function filterTickets() {
  const query = $('search').value.trim().toLocaleLowerCase();
  let count = 0;
  ticketButtons.forEach(button => {
    const t = examples[button.dataset.ticket];
    const matchesFilter = activeFilter === 'all' || (activeFilter === 'ready' ? t.state === 'ready' : t.state !== 'ready');
    const text = `${t.id} ${t.title} ${t.message} ${t.merchant} ${t.language} ${t.sources.map(s => s.text).join(' ')}`.toLocaleLowerCase();
    button.hidden = !(matchesFilter && (!query || text.includes(query)));
    if (!button.hidden) count++;
  });
  $('ticket-count').textContent = String(count);
  $('search-empty').hidden = count !== 0;
  ['all', 'ready', 'blocked'].forEach(key => {
    $(`filter-${key}`).setAttribute('aria-pressed', String(activeFilter === key));
    $(`filter-${key}`).classList.toggle('active', activeFilter === key);
  });
}

function insertDraft() {
  if ($('use-draft').disabled) return;
  $('editor').value = $('draft').value;
  hideReplacement();
  updateEditor();
  saveTicket();
  announce('Reviewed draft placed in your editor. No message sent.');
  $('editor').focus();
}

function requestInsertion() {
  if ($('use-draft').disabled) return;
  if ($('editor').value.trim() && $('editor').value !== $('draft').value) {
    $('replace-confirm').hidden = false;
    $('cancel-replace').focus();
    announce('Your editor already contains a reply. Choose whether to keep it or replace it with the reviewed suggestion.');
    return;
  }
  insertDraft();
}

function invalidatePacket() {
  $('packet').hidden = true;
  $('packet').replaceChildren();
  saveTicket();
}

ticketButtons.forEach(button => button.addEventListener('click', () => render(button.dataset.ticket)));
['all', 'ready', 'blocked'].forEach(key => $(`filter-${key}`).addEventListener('click', () => {
  activeFilter = key;
  filterTickets();
}));
$('search').addEventListener('input', filterTickets);
$('review').addEventListener('change', () => { hideReplacement(); updateApproval(); });
$('draft').addEventListener('input', () => {
  $('review').checked = false;
  hideReplacement();
  updateApproval();
  saveTicket();
});
$('editor').addEventListener('input', () => { hideReplacement(); updateEditor(); saveTicket(); });
$('manual-note').addEventListener('input', invalidatePacket);
$('reason').addEventListener('change', invalidatePacket);
$('use-draft').addEventListener('click', requestInsertion);
$('confirm-replace').addEventListener('click', insertDraft);
$('cancel-replace').addEventListener('click', () => { hideReplacement(); $('editor').focus(); announce('Existing reply kept.'); });
$('copy-reply').addEventListener('click', async () => {
  if (!$('editor').value.trim()) return;
  try {
    if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText($('editor').value);
    announce('Reply copied. Review it in your support inbox before sending.');
  } catch (_) {
    $('editor').focus();
    $('editor').select();
    announce('Automatic copying is unavailable. Your reply is selected; press Ctrl+C or ⌘C to copy.');
  }
});
$('escalate').addEventListener('click', () => {
  const t = examples[current];
  const reason = $('reason').value;
  const note = $('manual-note').value.trim();
  if (!reason) { announce('Choose a handover reason first.'); $('reason').focus(); return; }
  if (reason === 'Other — see agent note' && !note) { announce('Add an agent note for this handover reason.'); $('manual-note').focus(); return; }
  $('packet').hidden = false;
  $('packet').replaceChildren();
  const title = document.createElement('h2');
  title.textContent = `Handover preview · ${current === 'sensitive' ? 'Tier-2 compliance' : 'Tier-2 payments'}`;
  $('packet').append(title);
  for (const line of [
    `Ticket: ${t.id}`, `Verified merchant: ${t.merchant}`, `Reason: ${reason}`, `Gate: ${t.gate}`,
    `Authorized sources: ${t.sources.map(s => `${s.id} (snapshot fetched ${snapshotTime})`).join(', ') || 'none'}`,
    `Agent note: ${note || 'none'}`
  ]) {
    const paragraph = document.createElement('p');
    paragraph.textContent = line;
    $('packet').append(paragraph);
  }
  announce('Handover prepared in this workspace. Nothing sent to a real queue.');
  $('packet').focus();
  saveTicket();
});
$('manual').addEventListener('click', () => {
  manualMode = true;
  $('review').checked = false;
  hideReplacement();
  $('draft-panel').hidden = true;
  $('manual-state').hidden = false;
  $('manual').hidden = true;
  updateApproval();
  saveTicket();
  announce('Manual handling selected. Continue in your reply editor; no message sent.');
  $('editor').focus();
});
$('resume').addEventListener('click', () => {
  manualMode = false;
  // Re-render retains only this ticket’s text; source inspection and approval always reset.
  saveTicket();
  render(current);
  announce('Assisted review resumed. Inspect the sources and approve the reply again.');
});
$('reset').addEventListener('click', () => {
  initialized = false;
  buffers.clear();
  ticketButtons.forEach(button => { $(`saved-${button.dataset.ticket}`).hidden = true; });
  $('search').value = '';
  activeFilter = 'all';
  filterTickets();
  render('ready');
  announce('Demo reset. All in-tab drafts and notes cleared.');
});
function toggleShortcuts(open) {
  $('shortcut-panel').hidden = !open;
  $('shortcuts').setAttribute('aria-expanded', String(open));
}
$('shortcuts').addEventListener('click', () => toggleShortcuts($('shortcut-panel').hidden));
document.addEventListener('keydown', event => {
  const tag = event.target && event.target.tagName;
  const typing = ['INPUT', 'TEXTAREA', 'SELECT'].includes(tag) || (event.target && event.target.isContentEditable);
  if (event.key === 'Escape') {
    toggleShortcuts(false);
    hideReplacement();
    if (event.target === $('search')) { $('search').blur(); $('workspace').focus(); }
    return;
  }
  if (event.altKey && event.key === 'Enter') { event.preventDefault(); requestInsertion(); return; }
  if (typing || event.ctrlKey || event.metaKey || event.altKey) return;
  if (event.key === '/') { event.preventDefault(); $('search').focus(); }
  if (event.key.toLowerCase() === 'j' || event.key.toLowerCase() === 'k') {
    const visible = ticketButtons.filter(button => !button.hidden);
    if (!visible.length) return;
    event.preventDefault();
    const index = visible.findIndex(button => button.dataset.ticket === current);
    const next = index < 0 ? 0 : (index + (event.key.toLowerCase() === 'j' ? 1 : -1) + visible.length) % visible.length;
    render(visible[next].dataset.ticket);
    visible[next].focus();
  }
});
render('ready');
filterTickets();
