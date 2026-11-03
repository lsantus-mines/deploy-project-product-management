"use strict";
const D = FlowData,
  E = FlowEngine;
const $ = (id) => document.getElementById(id);
const STORAGE_KEY = "flowassist.workspace.v4";
const OUTCOMES = ["open", "waiting", "escalated", "resolved"];
let tickets = D.tickets.map((t) => ({ ...t }));
let records = new Map();
let current = "ready",
  currentView = "inbox",
  activeFilter = "all";
let inspectedSources = new Set(),
  manualMode = false,
  initialized = false;
let ticketButtons = [],
  analysis = null,
  pendingPacket = null,
  clockStarted = null;
let storageAvailable = true,
  timerPaused = false;
const blank = () => ({
  outcome: "open",
  priority: "Normal",
  reference: "",
  activeMs: 0,
  events: [],
  buffer: { editor: "", draft: null, note: "", reason: "", manual: false },
  receipt: null,
});
const node = (tag, text = "", className = "") => {
  const n = document.createElement(tag);
  n.textContent = text;
  if (className) n.className = className;
  return n;
};
const text = (value, limit = 3000) =>
  typeof value === "string" ? value.slice(0, limit) : "";
const duration = (ms) =>
  `${Math.floor(ms / 60000)}:${String(Math.floor(ms / 1000) % 60).padStart(2, "0")}`;
const record = () => records.get(current);
function announce(message) {
  $("status").textContent = message;
}

function loadWorkspace() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const saved = JSON.parse(raw);
    if (
      saved.version !== 4 ||
      !Array.isArray(saved.tickets) ||
      saved.tickets.length > 30 ||
      !Array.isArray(saved.records)
    )
      return;
    const known = new Set(D.accounts.map((a) => a.id)),
      keys = new Set();
    const restored = saved.tickets.map((t) => {
      if (
        !/^[a-z0-9-]{1,40}$/.test(t.key) ||
        keys.has(t.key) ||
        !/^DEMO-\d{2,4}$/.test(t.id) ||
        !known.has(t.merchant)
      )
        throw new Error("Invalid workspace");
      keys.add(t.key);
      return {
        key: t.key,
        id: t.id,
        merchant: t.merchant,
        title: E.sanitizeInput(text(t.title, 100)).text,
        message: E.sanitizeInput(text(t.message)).text,
        sensitiveInput:
          t.sensitiveInput === true || E.sanitizeInput(text(t.message)).flagged,
        language: ["EN", "FR", "DE", "PT"].includes(t.language)
          ? t.language
          : "EN",
        priority: t.priority === "High" ? "High" : "Normal",
        receivedAt: D.tickets[0].receivedAt,
      };
    });
    for (const [key, r] of saved.records) {
      if (!keys.has(key) || !r || typeof r !== "object") continue;
      const b = r.buffer || {};
      records.set(key, {
        ...blank(),
        outcome: OUTCOMES.includes(r.outcome) ? r.outcome : "open",
        priority: r.priority === "High" ? "High" : "Normal",
        reference: /^[A-Z0-9-]{1,60}$/.test(r.reference || "")
          ? r.reference
          : "",
        activeMs:
          Number.isFinite(r.activeMs) && r.activeMs >= 0
            ? Math.min(r.activeMs, 86400000)
            : 0,
        events: Array.isArray(r.events)
          ? r.events
              .slice(-100)
              .filter(
                (e) =>
                  e && typeof e.type === "string" && typeof e.at === "string",
              )
              .map((e) => ({
                type: text(e.type, 80),
                detail: text(e.detail, 500),
                at: text(e.at, 40),
              }))
          : [],
        buffer: {
          editor: E.sanitizeInput(text(b.editor, 10000)).text,
          draft:
            typeof b.draft === "string"
              ? E.sanitizeInput(text(b.draft, 10000)).text
              : null,
          note: E.sanitizeInput(text(b.note, 1500)).text,
          reason: text(b.reason, 100),
          manual: b.manual === true,
        },
        receipt:
          r.receipt && typeof r.receipt === "object"
            ? {
                kind: text(r.receipt.kind, 30),
                at: text(r.receipt.at, 40),
                text: E.sanitizeInput(text(r.receipt.text, 10000)).text,
              }
            : null,
      });
    }
    if (restored.length) tickets = restored;
  } catch (_) {
    records.clear();
    storageAvailable = false;
  }
}
function persist() {
  try {
    sessionStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ version: 4, tickets, records: [...records] }),
    );
  } catch (_) {
    storageAvailable = false;
  }
}
function event(type, detail = "") {
  const r = record();
  r.events.push({ type, detail, at: new Date().toISOString() });
  if (r.events.length > 100) r.events.shift();
  persist();
  renderEvents();
}
function flushClock() {
  if (clockStarted !== null) {
    record().activeMs += Math.max(0, Date.now() - clockStarted);
    clockStarted = null;
  }
}
function startClock() {
  if (
    currentView === "inbox" &&
    record().outcome === "open" &&
    !timerPaused &&
    !document.hidden &&
    $("new-ticket-panel").hidden &&
    $("export-preview").hidden &&
    clockStarted === null
  )
    clockStarted = Date.now();
}
function activeTime(key) {
  return (
    records.get(key).activeMs +
    (key === current && clockStarted !== null
      ? Math.max(0, Date.now() - clockStarted)
      : 0)
  );
}
function saveTicket() {
  if (!initialized) return;
  record().buffer = {
    draft: E.sanitizeInput($("draft").value).text,
    editor: E.sanitizeInput($("editor").value).text,
    note: E.sanitizeInput($("manual-note").value).text,
    reason: $("reason").value,
    manual: manualMode,
  };
  persist();
  const marker = $(`saved-${current}`);
  if (marker)
    marker.hidden = !(
      $("editor").value.trim() || $("manual-note").value.trim()
    );
}
function getAnalysis(key) {
  const t = tickets.find((t) => t.key === key);
  return E.analyze(t, D, records.get(key).reference);
}
function labelFor(a, r) {
  if (r.outcome !== "open")
    return {
      text: {
        waiting: "Awaiting merchant",
        escalated: "Handed over",
        resolved: "Resolved",
      }[r.outcome],
      className: r.outcome === "resolved" ? "ready-label" : "amber-label",
    };
  return {
    text:
      a.state === "draft_ready"
        ? "Reply ready"
        : a.intent === "dispute"
          ? "Dispute"
          : a.intent === "compliance"
            ? "Compliance"
            : a.gate.includes("unavailable")
              ? "Restricted"
              : "Needs review",
    className: a.state === "draft_ready" ? "ready-label" : "amber-label",
  };
}
function renderInbox() {
  $("ticket-list").replaceChildren();
  ticketButtons = [];
  tickets.forEach((t) => {
    const a = getAnalysis(t.key),
      r = records.get(t.key),
      label = labelFor(a, r);
    const b = node("button", "", "ticket");
    b.dataset.ticket = t.key;
    b.setAttribute("aria-pressed", String(current === t.key));
    const top = node("span", "", "ticket-top");
    top.append(
      node("span", t.id, "ticket-id"),
      node("span", label.text, `ticket-label ${label.className}`),
    );
    const bottom = node("span", "", "ticket-bottom");
    bottom.append(
      node("span", t.merchant.replace("M-", "").slice(0, 1), "merchant-avatar"),
      node("span", D.accounts.find((a) => a.id === t.merchant).name),
      node("span", t.language, "language"),
    );
    const saved = node("span", "Draft saved in this tab", "session-marker");
    saved.id = `saved-${t.key}`;
    saved.hidden = !(r.buffer.editor.trim() || r.buffer.note.trim());
    b.append(
      top,
      node("strong", t.title),
      node(
        "span",
        `${r.priority === "High" ? "High priority · " : ""}${t.message}`,
        "ticket-preview",
      ),
      bottom,
      saved,
    );
    b.addEventListener("click", () => {
      setView("inbox");
      render(t.key);
    });
    $("ticket-list").append(b);
    ticketButtons.push(b);
  });
  filterTickets();
}
function filterTickets() {
  const query = $("search").value.trim().toLocaleLowerCase();
  const counts = { all: tickets.length, ready: 0, blocked: 0, resolved: 0 };
  let visible = 0;
  ticketButtons.forEach((b) => {
    const t = tickets.find((t) => t.key === b.dataset.ticket),
      a = getAnalysis(t.key),
      r = records.get(t.key);
    const ready = a.state === "draft_ready" && r.outcome === "open";
    const done = ["resolved", "escalated"].includes(r.outcome);
    if (ready) counts.ready++;
    if (!ready && !done) counts.blocked++;
    if (done) counts.resolved++;
    const matches =
      activeFilter === "all" ||
      (activeFilter === "ready" && ready) ||
      (activeFilter === "blocked" && !ready && !done) ||
      (activeFilter === "resolved" && done);
    const haystack =
      `${t.id} ${t.title} ${t.message} ${t.merchant} ${r.reference} ${a.sources.map((s) => s.text).join(" ")}`.toLowerCase();
    b.hidden = !(matches && (!query || haystack.includes(query)));
    if (!b.hidden) visible++;
    b.setAttribute("aria-pressed", String(current === t.key));
  });
  $("ticket-count").textContent = String(visible);
  $("search-empty").hidden = visible !== 0;
  Object.keys(counts).forEach((key) => {
    $(`count-${key}`).textContent = String(counts[key]);
    $(`filter-${key}`).setAttribute(
      "aria-pressed",
      String(activeFilter === key),
    );
    $(`filter-${key}`).classList.toggle("active", activeFilter === key);
  });
}
function hideReplacement() {
  $("replace-confirm").hidden = true;
}
function updateEditor() {
  $("editor-count").textContent =
    `${$("editor").value.length.toLocaleString("en")} characters`;
  $("editor-state").textContent = $("editor").value.trim()
    ? "Draft · not sent"
    : "Not prepared";
  $("copy-reply").disabled =
    !$("editor").value.trim() || E.sanitizeInput($("editor").value).flagged;
  updateFinal();
}
function allSourcesChecked() {
  return (
    analysis.sources.length > 0 &&
    analysis.sources.every((s) => inspectedSources.has(s.id))
  );
}
function updateFinal() {
  const qa = E.evaluateDraft(analysis, $("editor").value);
  const available =
    analysis.state === "draft_ready" && record().outcome === "open";
  $("final-review").disabled = !available || !allSourcesChecked();
  $("record-reply").disabled = !(
    available &&
    allSourcesChecked() &&
    $("final-review").checked &&
    $("editor").value.trim() &&
    !qa.critical
  );
  $("final-check-result").textContent = !available
    ? "This case needs specialist handling, a reference, or reopening."
    : !$("editor").value.trim()
      ? "Prepare a reply, inspect its sources, then verify the final wording."
      : qa.passed
        ? "Final reply matches the source-backed wording. Human approval is still required."
        : qa.critical
          ? qa.issues.join(" ")
          : "Your edits require a manual factual review. Confirm the final review only after checking every claim.";
}
function updateApproval() {
  const qa = E.evaluateDraft(analysis, $("draft").value),
    all = allSourcesChecked(),
    open = record().outcome === "open";
  $("use-draft").disabled = !(
    analysis.state === "draft_ready" &&
    open &&
    !manualMode &&
    all &&
    $("review").checked &&
    qa.passed
  );
  $("draft-check-result").textContent = qa.passed
    ? "Source-backed wording passed the deterministic checks."
    : qa.issues.join(" ");
  $("draft-check-result").className = qa.passed
    ? "draft-check-result check-pass"
    : "draft-check-result check-fail";
  $("review-progress").textContent = manualMode
    ? "Assisted insertion paused."
    : !all
      ? `${inspectedSources.size}/${analysis.sources.length} source records inspected.`
      : !$("review").checked
        ? "Check the reply and confirm review."
        : "Ready to place in your editor. Nothing is sent.";
  const phase = !all
    ? "step-evidence"
    : !$("review").checked
      ? "step-review"
      : "step-reply";
  const order = ["step-evidence", "step-review", "step-reply"];
  order.forEach((id, i) => {
    $(id).setAttribute("aria-current", id === phase ? "step" : "false");
    $(id).classList.toggle("complete", i < order.indexOf(phase));
  });
  updateFinal();
}
function renderSources() {
  $("sources").replaceChildren();
  $("source-count").textContent = `${analysis.sources.length} records`;
  analysis.sources.forEach((s) => {
    const b = node(
      "button",
      `Open ${s.id} · ${s.id.startsWith("CLE") ? "Clearing" : "Ledger"}`,
    );
    b.setAttribute("aria-controls", "source-detail");
    b.setAttribute("aria-expanded", "false");
    b.addEventListener("click", () => {
      if (!inspectedSources.has(s.id)) event("Source inspected", s.id);
      inspectedSources.add(s.id);
      $("source-detail").hidden = false;
      $("source-detail").textContent = `${s.id}\n\n${s.text}`;
      Array.from($("sources").children).forEach((el) =>
        el.setAttribute("aria-expanded", "false"),
      );
      b.setAttribute("aria-expanded", "true");
      b.classList.add("inspected");
      b.textContent = `✓ ${s.id} · inspected`;
      updateApproval();
    });
    $("sources").append(b);
  });
  if (!analysis.sources.length)
    $("sources").append(
      node(
        "p",
        "No authorized transaction evidence available for this route.",
        "empty",
      ),
    );
  $("source-detail").hidden = true;
  $("source-detail").textContent = "";
}
function renderContext() {
  const a = analysis.account;
  $("account-context").replaceChildren();
  $("past-tickets").replaceChildren();
  $("policy-context").replaceChildren();
  if (a) {
    for (const [label, value] of [
      ["Merchant", a.name],
      ["Plan / region", `${a.plan} / ${a.region}`],
      ["KYC", a.kyc],
      ["PSD2 / SCA", a.sca],
    ]) {
      const row = node("div");
      row.append(node("span", label), node("strong", value));
      $("account-context").append(row);
    }
    a.history.forEach((h) => {
      const card = node("article", "", "context-item");
      card.append(
        node("strong", `${h.id} · ${h.title}`),
        node("p", h.outcome),
        node("small", h.date),
      );
      $("past-tickets").append(card);
    });
  }
  D.policies.forEach((p) => {
    const item = node("article", "", "context-item");
    item.append(node("strong", `${p.id} · ${p.title}`), node("p", p.text));
    $("policy-context").append(item);
  });
  $("analysis-checks").replaceChildren();
  const checks =
    analysis.state === "draft_ready"
      ? analysis.checks
      : [analysis.gate, analysis.reason];
  checks.forEach((c) =>
    $("analysis-checks").append(
      node("p", `${analysis.state === "draft_ready" ? "✓ " : ""}${c}`),
    ),
  );
  $("summary-panel").hidden = !analysis.transaction;
  if (!analysis.transaction) return;
  const tx = analysis.transaction;
  $("payment-amount").textContent = E.money(tx.amountMinor, tx.currency);
  $("payment-reference").textContent = tx.id;
  $("invoice-reference").textContent = tx.reference;
  $("payment-status").textContent = tx.status.replace(/_/g, " ");
  $("payment-status").className = "ticket-label ready-label";
  $("payment-timeline").replaceChildren();
  const events = [
    ["Merchant match verified", `${tx.merchant} · ${tx.reference}`],
    [tx.status.replace(/_/g, " "), `${E.stamp(tx.eventAt)} · ${tx.clearing}`],
  ];
  if (tx.feeMinor)
    events.push([
      "Documented fee reconciliation",
      `${E.money(tx.amountMinor, tx.currency)} − ${E.money(tx.feeMinor, tx.currency)} = ${E.money(tx.netMinor, tx.currency)}`,
    ]);
  if (["sent_to_bank", "pending"].includes(tx.status))
    events.push([
      "Beneficiary credit unconfirmed",
      "No arrival or settlement time is promised.",
    ]);
  if (tx.status === "returned")
    events.push([
      "Account credit unconfirmed",
      "Return is not proof of money credited back.",
    ]);
  events.forEach(([title, detail], i) => {
    const li = node("li", "", "timeline-done");
    li.append(node("span", "", "timeline-point"));
    const div = node("div");
    div.append(node("strong", title), node("span", detail));
    li.append(div);
    $("payment-timeline").append(li);
  });
  $("snapshot-note").textContent =
    `Fixture snapshot · ${E.stamp(tx.fetchedAt)} · not a live payment status`;
}
function renderEvents() {
  $("case-events").replaceChildren();
  const events = record().events;
  if (!events.length)
    $("case-events").append(
      node(
        "p",
        "No action recorded yet. Inspect evidence to start the review.",
        "section-description",
      ),
    );
  events
    .slice()
    .reverse()
    .forEach((e) => {
      const item = node("div", "", "event-item");
      item.append(
        node("strong", e.type),
        node("p", e.detail),
        node("small", new Date(e.at).toLocaleTimeString("en-GB")),
      );
      $("case-events").append(item);
    });
}
function render(key) {
  if (!tickets.some((t) => t.key === key)) return;
  flushClock();
  saveTicket();
  current = key;
  analysis = getAnalysis(key);
  inspectedSources = new Set();
  pendingPacket = null;
  const t = tickets.find((t) => t.key === key),
    r = record(),
    b = r.buffer;
  manualMode = b.manual;
  document.title = `${t.id} · FlowAssist`;
  $("ticket-meta").textContent = `${t.id} · ${t.language}`;
  $("ticket-title").textContent = t.title;
  $("message").textContent = t.message;
  $("merchant").textContent = `Assigned demo merchant · ${t.merchant}`;
  $("message-language").textContent = {
    EN: "English",
    FR: "Français",
    DE: "Deutsch",
    PT: "Português",
  }[t.language];
  $("sender-name").textContent = analysis.account
    ? `${analysis.account.name} · finance team`
    : "Merchant request";
  $("sender-avatar").textContent = t.merchant.replace("M-", "").slice(0, 1);
  $("case-status").textContent = {
    open: "Open · assigned to you",
    waiting: "Awaiting merchant reference",
    escalated: "Handed over · specialist queue",
    resolved: "Resolved · demo reply recorded",
  }[r.outcome];
  $("priority").value = r.priority;
  $("reopen").hidden = r.outcome === "open";
  $("gate").textContent = analysis.gate;
  $("gate").className =
    analysis.state === "draft_ready" ? "safe" : "safe gate-warning";
  $("blocked").hidden = analysis.state === "draft_ready";
  $("blocked").textContent = analysis.reason;
  $("draft").value = b.draft === null ? analysis.draft || "" : b.draft;
  $("draft-panel").hidden =
    analysis.state !== "draft_ready" || manualMode || r.outcome !== "open";
  $("editor").value = b.editor;
  $("manual-note").value = b.note;
  $("reason").value = b.reason;
  $("review").checked = false;
  $("final-review").checked = false;
  $("manual-state").hidden = !manualMode;
  $("manual").hidden = manualMode || r.outcome !== "open";
  $("handover").open = analysis.state !== "draft_ready";
  $("handover-destination").textContent =
    `Prepare context for ${analysis.queue}. No real queue is contacted.`;
  $("packet").hidden = true;
  $("packet").replaceChildren();
  $("record-handover").hidden = true;
  $("reference-panel").hidden =
    analysis.intent !== "tracing" ||
    analysis.state !== "context_only" ||
    analysis.transaction !== null ||
    r.outcome !== "open" ||
    !analysis.gate.toLowerCase().includes("reference");
  $("confirmed-reference").value = r.reference;
  $("reference-confirmed").checked = false;
  hideReplacement();
  renderSources();
  renderContext();
  renderEvents();
  initialized = true;
  updateEditor();
  updateApproval();
  filterTickets();
  startClock();
  $("work-clock").textContent = `${duration(activeTime(key))} active`;
  announce(
    b.editor
      ? "This ticket’s draft restored. Source inspection and approval reset."
      : !storageAvailable
        ? "Browser saving unavailable; this workspace stays in memory only."
        : "",
  );
}
function refresh(message) {
  saveTicket();
  renderInbox();
  render(current);
  if (message) announce(message);
}
function insertDraft() {
  updateApproval();
  if ($("use-draft").disabled) return;
  $("editor").value = $("draft").value;
  $("final-review").checked = false;
  hideReplacement();
  updateEditor();
  saveTicket();
  event("Reviewed draft inserted", "No message sent.");
  announce(
    "Reviewed draft placed in your editor. Verify the final reply before recording completion.",
  );
  $("editor").focus();
}
function requestInsertion() {
  updateApproval();
  if ($("use-draft").disabled) return;
  if ($("editor").value.trim() && $("editor").value !== $("draft").value) {
    $("replace-confirm").hidden = false;
    $("cancel-replace").focus();
    announce("Choose whether to keep or replace your existing reply.");
    return;
  }
  insertDraft();
}
function invalidatePacket() {
  $("packet").hidden = true;
  $("packet").replaceChildren();
  $("record-handover").hidden = true;
  pendingPacket = null;
  saveTicket();
}
function setView(view) {
  flushClock();
  saveTicket();
  currentView = view;
  $("view-label").textContent = {
    inbox: "Assigned inbox",
    activity: "Activity trail",
    metrics: "Session overview",
  }[view];
  document.title =
    view === "inbox"
      ? `${tickets.find((t) => t.key === current).id} · FlowAssist`
      : `${$("view-label").textContent} · FlowAssist`;
  ["inbox", "activity", "metrics"].forEach((v) => {
    $(`${v}-view`).hidden = v !== view;
    $(`nav-${v}`).setAttribute("aria-pressed", String(v === view));
    $(`nav-${v}`).classList.toggle("rail-active", v === view);
    $(`mobile-${v}`).setAttribute("aria-pressed", String(v === view));
  });
  if (view === "activity") renderAudit();
  if (view === "metrics") renderMetrics();
  startClock();
  persist();
}
function auditRows() {
  return tickets
    .flatMap((t) =>
      records
        .get(t.key)
        .events.map((e) => ({ ticket: t.id, merchant: t.merchant, ...e })),
    )
    .sort((a, b) => b.at.localeCompare(a.at));
}
function renderAudit() {
  $("audit-list").replaceChildren();
  const events = auditRows();
  if (!events.length)
    $("audit-list").append(
      node(
        "p",
        "Your decisions and reviews will appear here as you work through cases.",
        "empty",
      ),
    );
  events.forEach((e) => {
    const row = node("article", "", "audit-row");
    row.append(
      node("span", e.ticket, "subtle-tag"),
      node("strong", e.type),
      node("p", e.detail),
      node(
        "small",
        `${e.merchant} · ${new Date(e.at).toLocaleString("en-GB")}`,
      ),
    );
    $("audit-list").append(row);
  });
}
function renderMetrics() {
  $("metric-cards").replaceChildren();
  $("metrics-rows").replaceChildren();
  const completed = tickets.filter((t) =>
    ["resolved", "escalated"].includes(records.get(t.key).outcome),
  );
  const mean = completed.length
    ? duration(
        completed.reduce((sum, t) => sum + activeTime(t.key), 0) /
          completed.length,
      )
    : "—";
  const values = [
    ["Cases", tickets.length],
    [
      "Replies recorded",
      tickets.filter((t) => records.get(t.key).outcome === "resolved").length,
    ],
    [
      "Specialist handovers",
      tickets.filter((t) => records.get(t.key).outcome === "escalated").length,
    ],
    [
      "Active work",
      duration(tickets.reduce((sum, t) => sum + activeTime(t.key), 0)),
    ],
    ["Mean completion", mean],
  ];
  values.forEach(([label, value]) => {
    const card = node("article", "", "metric-card");
    card.append(node("span", label), node("strong", String(value)));
    $("metric-cards").append(card);
  });
  tickets.forEach((t) => {
    const tr = node("tr"),
      r = records.get(t.key),
      a = getAnalysis(t.key);
    [
      t.id,
      t.merchant,
      {
        draft_ready: "Reply review",
        context_only: "Context only",
        human_only: "Specialist",
      }[a.state],
      {
        open: "Open",
        waiting: "Awaiting merchant",
        escalated: "Handed over",
        resolved: "Resolved",
      }[r.outcome],
      duration(activeTime(t.key)),
    ].forEach((value) => tr.append(node("td", value)));
    $("metrics-rows").append(tr);
  });
}
function exportData(name, content, type) {
  $("export-preview").hidden = false;
  $("export-text").value = content;
  try {
    const url = URL.createObjectURL(new Blob([content], { type }));
    const a = node("a");
    a.href = url;
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  } catch (_) {
    announce("Export is available in the preview for manual copying.");
  }
}
function recordedHandover(ticket, receipt) {
  if (!receipt || receipt.kind !== "handover") return null;
  try {
    const packet = JSON.parse(receipt.text);
    if (packet.ticket !== ticket.id || packet.merchant !== ticket.merchant)
      return null;
    const allowed = new Set(analysis.sources.map((source) => source.id));
    return {
      at: receipt.at,
      queue: analysis.queue,
      reason: text(packet.reason, 100),
      note: E.sanitizeInput(text(packet.note, 1500)).text,
      sources: Array.isArray(packet.sources)
        ? packet.sources
            .filter((source) => source && allowed.has(source.id))
            .map((source) => ({
              id: source.id,
              fetchedAt: text(source.fetchedAt, 40),
            }))
        : [],
    };
  } catch (_) {
    return null;
  }
}
function receipt() {
  const t = tickets.find((t) => t.key === current),
    r = record();
  return {
    version: 4,
    demo: true,
    ticket: t.id,
    merchant: t.merchant,
    outcome: r.outcome,
    route: analysis.state,
    queue: analysis.queue,
    policy: "FLOW-POL-1",
    activeMs: Math.round(activeTime(current)),
    sources: analysis.sources.map((s) => ({
      id: s.id,
      merchant: s.merchant,
      fetchedAt: s.fetchedAt,
    })),
    events: r.events,
    handover: recordedHandover(t, r.receipt),
    reply: r.receipt && r.receipt.kind === "reply" ? r.receipt : null,
  };
}

loadWorkspace();
tickets.forEach((t) => {
  if (!records.has(t.key))
    records.set(t.key, { ...blank(), priority: t.priority });
});
["all", "ready", "blocked", "resolved"].forEach((key) =>
  $(`filter-${key}`).addEventListener("click", () => {
    activeFilter = key;
    filterTickets();
  }),
);
$("search").addEventListener("input", filterTickets);
$("review").addEventListener("change", () => {
  hideReplacement();
  updateApproval();
});
$("draft").addEventListener("input", () => {
  $("review").checked = false;
  hideReplacement();
  updateApproval();
  saveTicket();
});
$("restore-draft").addEventListener("click", () => {
  $("draft").value = analysis.draft || "";
  $("review").checked = false;
  updateApproval();
  saveTicket();
  announce("Original source-backed wording restored. Review again.");
});
$("editor").addEventListener("input", () => {
  $("final-review").checked = false;
  hideReplacement();
  updateEditor();
  saveTicket();
});
$("final-review").addEventListener("change", updateFinal);
$("manual-note").addEventListener("input", invalidatePacket);
$("reason").addEventListener("change", invalidatePacket);
$("use-draft").addEventListener("click", requestInsertion);
$("confirm-replace").addEventListener("click", insertDraft);
$("cancel-replace").addEventListener("click", () => {
  hideReplacement();
  $("editor").focus();
});
$("copy-reply").addEventListener("click", async () => {
  if ($("copy-reply").disabled) return;
  try {
    if (!navigator.clipboard) throw new Error();
    await navigator.clipboard.writeText($("editor").value);
    announce("Reply copied. Nothing sent.");
  } catch (_) {
    $("editor").focus();
    $("editor").select();
    announce("Reply selected. Press Ctrl+C or ⌘C to copy.");
  }
});
$("manual").addEventListener("click", () => {
  manualMode = true;
  $("review").checked = false;
  event("Manual handling selected");
  refresh(
    "Manual handling active. Check every final claim before recording a reply.",
  );
  $("editor").focus();
});
$("resume").addEventListener("click", () => {
  manualMode = false;
  refresh("Assisted review resumed. Inspect sources and approve again.");
});
$("pause-timer").addEventListener("click", () => {
  flushClock();
  timerPaused = !timerPaused;
  $("pause-timer").textContent = timerPaused ? "Resume timing" : "Pause timing";
  persist();
  startClock();
  announce(
    timerPaused
      ? "Handling timer paused for an interruption."
      : "Handling timer resumed.",
  );
});
$("priority").addEventListener("change", () => {
  record().priority = $("priority").value === "High" ? "High" : "Normal";
  event("Priority changed", record().priority);
  renderInbox();
});
$("resolve-reference").addEventListener("click", () => {
  if (
    !$("reference-confirmed").checked ||
    !$("confirmed-reference").value.trim()
  ) {
    announce("Confirm that the merchant supplied a unique reference first.");
    return;
  }
  const ref = $("confirmed-reference").value.trim().toUpperCase();
  if (!/^[A-Z0-9-]{1,60}$/.test(ref)) {
    announce("Use a valid reference containing letters, numbers and hyphens.");
    return;
  }
  const t = tickets.find((t) => t.key === current),
    check = E.analyze(t, D, ref);
  if (check.state !== "draft_ready") {
    announce(`${check.gate}. ${check.reason}`);
    return;
  }
  record().reference = ref;
  record().outcome = "open";
  record().buffer.draft = null;
  event("Merchant reference verified", ref);
  initialized = false;
  refresh(
    "Unique payment confirmed from the merchant’s reference. Inspect the sources and draft.",
  );
});
$("wait-reference").addEventListener("click", () => {
  record().outcome = "waiting";
  event(
    "Awaiting merchant",
    "Unique reference requested by the human operator; no automatic message sent.",
  );
  refresh(
    "Case marked awaiting merchant. Reopen it when the reference arrives.",
  );
});
$("reopen").addEventListener("click", () => {
  record().outcome = "open";
  event("Case reopened");
  refresh("Case reopened. Source review and final approval reset.");
});
$("escalate").addEventListener("click", () => {
  if (["resolved", "escalated"].includes(record().outcome)) {
    announce("Reopen the case before preparing a new handover.");
    return;
  }
  try {
    pendingPacket = E.handover(
      tickets.find((t) => t.key === current),
      analysis,
      $("reason").value,
      $("manual-note").value,
    );
  } catch (error) {
    announce(error.message);
    $("reason").focus();
    return;
  }
  $("packet").replaceChildren();
  $("packet").hidden = false;
  $("packet").append(node("h2", `Handover preview · ${pendingPacket.queue}`));
  for (const line of [
    `Ticket: ${pendingPacket.ticket}`,
    `Verified merchant: ${pendingPacket.merchant}`,
    `Reason: ${pendingPacket.reason}`,
    `Gate: ${pendingPacket.gate}`,
    `Authorized sources: ${pendingPacket.sources.map((s) => `${s.id} (snapshot fetched ${s.fetchedAt})`).join(", ") || "none"}`,
    `Agent note: ${pendingPacket.note || "none"}`,
  ])
    $("packet").append(node("p", line));
  $("record-handover").hidden = false;
  $("packet").focus();
  announce(
    "Handover preview prepared. Review it, then record the transfer in the demo.",
  );
});
$("record-handover").addEventListener("click", () => {
  if (!pendingPacket) return;
  record().outcome = "escalated";
  record().receipt = {
    kind: "handover",
    at: new Date().toISOString(),
    text: JSON.stringify(pendingPacket),
  };
  event(
    "Specialist handover recorded",
    `${pendingPacket.queue} · ${pendingPacket.reason} · demo only`,
  );
  refresh("Specialist handover recorded. No real queue was contacted.");
});
$("record-reply").addEventListener("click", () => {
  updateFinal();
  if ($("record-reply").disabled) return;
  flushClock();
  record().receipt = {
    kind: "reply",
    at: new Date().toISOString(),
    text: $("editor").value,
  };
  record().outcome = "resolved";
  event(
    "Human reply recorded",
    "Final reply explicitly reviewed by the operator; demo completion, no message sent.",
  );
  refresh(
    "Human-reviewed reply recorded and case resolved in the demo. No customer message was sent.",
  );
});
["inbox", "activity", "metrics"].forEach((v) => {
  $(`nav-${v}`).addEventListener("click", () => setView(v));
  $(`mobile-${v}`).addEventListener("click", () => setView(v));
});
$("new-ticket").addEventListener("click", () => {
  flushClock();
  $("new-ticket-panel").hidden = false;
  $("intake-title").focus();
});
$("cancel-ticket").addEventListener("click", () => {
  $("new-ticket-panel").hidden = true;
  startClock();
});
$("intake-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const title = $("intake-title").value.trim(),
    message = $("intake-message").value.trim(),
    merchant = $("intake-merchant").value,
    language = $("intake-language").value;
  if (
    !title ||
    !message ||
    title.length > 100 ||
    message.length > 3000 ||
    !D.accounts.some((a) => a.id === merchant) ||
    !["EN", "FR", "DE", "PT"].includes(language)
  ) {
    $("intake-error").textContent =
      "Choose a demo merchant and language, and provide a subject and message.";
    return;
  }
  if (tickets.length >= 30) {
    $("intake-error").textContent =
      "This demo supports 30 cases. Export your work before resetting.";
    return;
  }
  const number =
      Math.max(...tickets.map((t) => Number(t.id.replace("DEMO-", "")))) + 1,
    key = `custom-${number}`;
  const safeMessage = E.sanitizeInput(message),
    safeTitle = E.sanitizeInput(title);
  saveTicket();
  flushClock();
  tickets.push({
    key,
    id: `DEMO-${String(number).padStart(2, "0")}`,
    merchant,
    language,
    title: safeTitle.text,
    message: safeMessage.text,
    sensitiveInput: safeMessage.flagged || safeTitle.flagged,
    priority: $("intake-priority").value === "High" ? "High" : "Normal",
    receivedAt: D.tickets[0].receivedAt,
  });
  records.set(key, {
    ...blank(),
    priority: $("intake-priority").value === "High" ? "High" : "Normal",
  });
  $("new-ticket-panel").hidden = true;
  $("intake-title").value = "";
  $("intake-message").value = "";
  $("intake-error").textContent = "";
  $("search").value = "";
  activeFilter = "all";
  renderInbox();
  setView("inbox");
  render(key);
  event(
    "Case created",
    "Synthetic request analyzed against the assigned merchant fixtures.",
  );
  announce(
    "Case created and investigated. Review the evidence or follow the specialist route.",
  );
});
$("export-case").addEventListener("click", () => {
  flushClock();
  exportData(
    `${tickets.find((t) => t.key === current).id}-receipt.json`,
    JSON.stringify(receipt(), null, 2),
    "application/json",
  );
  startClock();
});
$("export-audit").addEventListener("click", () =>
  exportData(
    "flowassist-audit.json",
    JSON.stringify(
      { demo: true, policy: "FLOW-POL-1", events: auditRows() },
      null,
      2,
    ),
    "application/json",
  ),
);
$("export-metrics").addEventListener("click", () => {
  const rows = [
    ["ticket", "merchant", "outcome", "active_seconds"],
    ...tickets.map((t) => [
      t.id,
      t.merchant,
      records.get(t.key).outcome,
      Math.round(activeTime(t.key) / 1000),
    ]),
  ];
  exportData(
    "flowassist-timings.csv",
    rows
      .map((row) =>
        row.map((v) => `"${String(v).replace(/"/g, '""')}"`).join(","),
      )
      .join("\n"),
    "text/csv",
  );
});
$("close-export").addEventListener("click", () => {
  $("export-preview").hidden = true;
  startClock();
});
$("reset").addEventListener("click", () => {
  flushClock();
  initialized = false;
  records.clear();
  tickets = D.tickets.map((t) => ({ ...t }));
  tickets.forEach((t) =>
    records.set(t.key, { ...blank(), priority: t.priority }),
  );
  current = "ready";
  activeFilter = "all";
  timerPaused = false;
  $("pause-timer").textContent = "Pause timing";
  $("search").value = "";
  $("new-ticket-panel").hidden = true;
  $("export-preview").hidden = true;
  renderInbox();
  setView("inbox");
  render("ready");
  persist();
  announce("Demo reset. All local work, custom cases and receipts cleared.");
});
function toggleShortcuts(open) {
  $("shortcut-panel").hidden = !open;
  $("shortcuts").setAttribute("aria-expanded", String(open));
}
$("shortcuts").addEventListener("click", () =>
  toggleShortcuts($("shortcut-panel").hidden),
);
document.addEventListener("keydown", (e) => {
  const typing =
    ["INPUT", "TEXTAREA", "SELECT"].includes(e.target && e.target.tagName) ||
    (e.target && e.target.isContentEditable);
  if (e.key === "Escape") {
    toggleShortcuts(false);
    hideReplacement();
    $("new-ticket-panel").hidden = true;
    startClock();
    if (e.target === $("search")) {
      $("search").blur();
      $("workspace").focus();
    }
    return;
  }
  if (
    e.altKey &&
    e.key === "Enter" &&
    currentView === "inbox" &&
    $("new-ticket-panel").hidden &&
    $("export-preview").hidden
  ) {
    e.preventDefault();
    requestInsertion();
    return;
  }
  if (typing || e.ctrlKey || e.metaKey || e.altKey) return;
  if (e.key === "/") {
    e.preventDefault();
    $("search").focus();
  }
  if (["j", "k"].includes(e.key.toLowerCase())) {
    const visible = ticketButtons.filter((b) => !b.hidden);
    if (!visible.length) return;
    e.preventDefault();
    const index = visible.findIndex((b) => b.dataset.ticket === current),
      next =
        index < 0
          ? 0
          : (index + (e.key.toLowerCase() === "j" ? 1 : -1) + visible.length) %
            visible.length;
    setView("inbox");
    render(visible[next].dataset.ticket);
    visible[next].focus();
  }
});
document.addEventListener("visibilitychange", () => {
  flushClock();
  persist();
  startClock();
});
if (typeof window !== "undefined")
  window.addEventListener("pagehide", () => {
    flushClock();
    saveTicket();
    persist();
  });
setInterval(() => {
  if (currentView === "inbox")
    $("work-clock").textContent =
      `${duration(activeTime(current))} ${record().outcome !== "open" ? "recorded" : clockStarted === null ? "paused" : "active"}`;
}, 1000);
renderInbox();
render(tickets.some((t) => t.key === "ready") ? "ready" : tickets[0].key);
setView("inbox");
