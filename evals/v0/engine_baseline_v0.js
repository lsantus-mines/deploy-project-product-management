/* Pure local domain logic. Deterministic demo checks, not an LLM or bank API. */
(() => {
  "use strict";
  const money = (minor, currency) =>
    `${currency} ${(minor / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  const stamp = (date) =>
    date && Number.isFinite(Date.parse(date))
      ? new Date(date).toISOString().slice(0, 16).replace("T", " ") + " UTC"
      : "Timestamp unavailable";
  const normalize = (text) =>
    text
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();
  function parseMinor(value) {
    let cleaned = String(value).replace(/\s/g, "");
    if (/^\d{1,3}(,\d{3})+(\.\d{1,2})?$/.test(cleaned))
      cleaned = cleaned.replace(/,/g, "");
    else if (/^\d+(,\d{1,2})$/.test(cleaned))
      cleaned = cleaned.replace(",", ".");
    if (!/^\d+(\.\d{1,2})?$/.test(cleaned)) return null;
    const [whole, fraction = ""] = cleaned.split(".");
    const minor = Number(whole) * 100 + Number(fraction.padEnd(2, "0"));
    return Number.isSafeInteger(minor) && minor > 0 ? minor : null;
  }
  function entities(text) {
    const amounts = [];
    let invalidAmount = false;
    const re =
      /(?:\b(EUR|USD)\s*|([€$])\s*)(\d[\d\s,.]*\d|\d)|\b(\d[\d\s,.]*\d|\d)\s*(EUR|USD|euros?)\b/gi;
    for (const m of text.matchAll(re)) {
      const minor = parseMinor((m[3] || m[4]).trim());
      const token = (m[1] || m[2] || m[5]).toUpperCase();
      if (minor !== null)
        amounts.push({
          minor,
          currency: ["$", "USD"].includes(token) ? "USD" : "EUR",
        });
      else invalidAmount = true;
    }
    const references = [
      ...new Set(
        text
          .toUpperCase()
          .match(
            /\b(?:INV|TX|SWIFT|RETURN|NET|STALE|CHECK|BETA)-[A-Z0-9-]+\b/g,
          ) || [],
      ),
    ];
    return { amounts, references, invalidAmount };
  }
  function sanitizeInput(value) {
    let flagged = false;
    const safe = String(value).replace(
      /(password|mot de passe|passwort|api[_ -]?key)\s*[:=]\s*[^\s,;]+|\bsk_live_[A-Za-z0-9_]+|\bFAKE_SECRET[A-Za-z0-9_]*|\b[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]){11,30}\b/gi,
      () => {
        flagged = true;
        return "[REDACTED_SECRET]";
      },
    );
    return {
      text: safe,
      flagged: flagged || safe.includes("[REDACTED_SECRET]"),
    };
  }
  function classify(text) {
    const n = normalize(text);
    if (
      /\b(kyc|aml|compliance|fraud|fraude|betrug)\b|freigeben|geben sie sie frei|frozen|hold.{0,20}release|release.{0,20}hold/.test(
        n,
      )
    )
      return "compliance";
    if (/chargeback|disput|contestation|litige/.test(n)) return "dispute";
    if (
      /refund|rembours|release.{0,15}fund|transfer.{0,10}now|execute.{0,10}payment/.test(
        n,
      )
    )
      return "money_action";
    return "tracing";
  }
  function sourceRecords(tx) {
    return [
      {
        id: tx.ledger,
        merchant: tx.merchant,
        transaction: tx.id,
        fetchedAt: tx.fetchedAt,
        text: `${tx.merchant} · ${tx.id} · ${tx.reference}\n${money(tx.amountMinor, tx.currency)} · ${tx.status}\n${tx.feeMinor ? `Documented fee: ${money(tx.feeMinor, tx.currency)} · net: ${money(tx.netMinor, tx.currency)}\n` : ""}Fetched: ${stamp(tx.fetchedAt)}`,
      },
      {
        id: tx.clearing,
        merchant: tx.merchant,
        transaction: tx.id,
        fetchedAt: tx.fetchedAt,
        text: `${tx.merchant} · ${tx.id} · ${tx.rail}\nStatus: ${tx.clearingStatus || tx.status}\nEvent: ${stamp(tx.eventAt)}\n${tx.status === "sent_to_bank" ? "Beneficiary credit: NOT confirmed\n" : ""}Fetched: ${stamp(tx.fetchedAt)}`,
      },
    ];
  }
  function makeDraft(ticket, tx) {
    const amount = money(tx.amountMinor, tx.currency),
      date = stamp(tx.eventAt),
      citations = `[${tx.ledger}; ${tx.clearing}]`;
    const en = {
      pending: `is pending as of ${date}. No beneficiary credit is confirmed.`,
      sent_to_bank: `was sent to the bank on ${date}. Beneficiary credit is not yet confirmed.`,
      credited: `was credited on ${date}.`,
      failed: `failed on ${date}. The available records do not specify a reason or a refund date.`,
      returned: `was returned on ${date}. A credit back to your account is not confirmed.`,
    };
    const fr = {
      pending: `est en attente au ${date}. Le crédit au bénéficiaire n’est pas confirmé.`,
      sent_to_bank: `a été transmis à la banque le ${date}. Le crédit au bénéficiaire n’est pas confirmé.`,
      credited: `a été crédité le ${date}.`,
      failed: `a échoué le ${date}. Les sources ne précisent ni motif ni date de remboursement.`,
      returned: `a été retourné le ${date}. Le recrédit de votre compte n’est pas confirmé.`,
    };
    const de = {
      pending: `ist zum ${date} ausstehend. Eine Gutschrift beim Empfänger ist nicht bestätigt.`,
      sent_to_bank: `wurde am ${date} an die Bank übermittelt. Eine Gutschrift beim Empfänger ist nicht bestätigt.`,
      credited: `wurde am ${date} gutgeschrieben.`,
      failed: `ist am ${date} fehlgeschlagen. Die Unterlagen nennen weder einen Grund noch einen Erstattungstermin.`,
      returned: `wurde am ${date} zurückgegeben. Eine Kontogutschrift ist nicht bestätigt.`,
    };
    const prefix =
      ticket.language === "FR"
        ? "Votre paiement"
        : ticket.language === "DE"
          ? "Ihre Zahlung"
          : "Your payment";
    if (tx.feeMinor && tx.status === "credited") {
      const fee = money(tx.feeMinor, tx.currency),
        net = money(tx.netMinor, tx.currency),
        ref = `(${tx.reference}, ${tx.id})`;
      return ticket.language === "FR"
        ? `Votre paiement brut ${amount} ${ref} comporte des frais documentés de ${fee}. Le montant net ${net} a été crédité le ${date}. ${citations}`
        : ticket.language === "DE"
          ? `Ihre Bruttozahlung ${amount} ${ref} hat eine dokumentierte Gebühr von ${fee}. Der Nettobetrag ${net} wurde am ${date} gutgeschrieben. ${citations}`
          : `Your gross payment ${amount} ${ref} has a documented fee of ${fee}. The net amount ${net} was credited on ${date}. ${citations}`;
    }
    let reply = `${prefix} ${amount} (${tx.reference}, ${tx.id}) ${(ticket.language === "FR" ? fr : ticket.language === "DE" ? de : en)[tx.status]} ${citations}`;
    if (tx.feeMinor)
      reply +=
        ticket.language === "FR"
          ? ` Montant brut ${amount}, frais documentés ${money(tx.feeMinor, tx.currency)}, montant net documenté ${money(tx.netMinor, tx.currency)}. ${citations}`
          : ticket.language === "DE"
            ? ` Bruttobetrag ${amount}, dokumentierte Gebühr ${money(tx.feeMinor, tx.currency)}, dokumentierter Nettobetrag ${money(tx.netMinor, tx.currency)}. ${citations}`
            : ` Gross amount ${amount}, documented fee ${money(tx.feeMinor, tx.currency)}, documented net amount ${money(tx.netMinor, tx.currency)}. ${citations}`;
    return reply;
  }
  function analyze(ticket, data, confirmedReference = "") {
    const account = data.accounts.find((a) => a.id === ticket.merchant);
    const extracted = entities(ticket.message);
    const intent = classify(ticket.message);
    const base = {
      account: account || null,
      intent,
      entities: extracted,
      candidates: [],
      sources: [],
      transaction: null,
      draft: null,
      state: "context_only",
      queue: "Tier-2 payments",
      checks: [],
      reason: "",
      gate: "",
    };
    const block = (
      gate,
      reason,
      state = "context_only",
      queue = "Tier-2 payments",
    ) => ({ ...base, gate, reason, state, queue });
    if (!account)
      return block(
        "Merchant scope unavailable",
        "No account context or transaction evidence is available.",
        "human_only",
      );
    if (!["EN", "FR", "DE"].includes(ticket.language))
      return block(
        "Language specialist needed",
        "This language is outside the supported demo languages.",
        "human_only",
      );
    if (
      /ignore.{0,30}(session|scope|tenant)|admin override|system:|reveal.{0,20}other merchant/i.test(
        ticket.message,
      )
    )
      return block(
        "Unsafe instruction blocked",
        "Ticket instructions cannot change merchant scope. No draft is generated.",
        "human_only",
      );
    if (ticket.sensitiveInput || sanitizeInput(ticket.message).flagged)
      return block(
        "Sensitive input needs manual handling",
        "No generation or message-body export is available for this input.",
        "human_only",
      );
    if (intent !== "tracing")
      return block(
        intent === "dispute"
          ? "Dispute specialist required"
          : intent === "compliance"
            ? "Compliance specialist required"
            : "Financial action requires a specialist",
        "Account context is available. No deadline, regulatory diagnosis, hold release, refund or execution advice is generated.",
        "human_only",
        intent === "dispute"
          ? "Tier-2 disputes"
          : intent === "compliance"
            ? "Tier-2 compliance"
            : "Tier-2 payments",
      );
    if (account.kyc !== "Verified")
      return block(
        "Account review flag needs a specialist",
        "The account carries a review flag. No diagnosis or release advice is generated.",
        "human_only",
        "Tier-2 compliance",
      );
    if (
      extracted.invalidAmount ||
      /\b(?:GBP|JPY|CHF|CAD)\b|[£¥]|(?:EUR|USD|€|\$)\s*[-−]|[-−]\s*\d[\d ,.]*\s*(?:EUR|USD)/i.test(
        ticket.message,
      )
    )
      return block(
        "Unsupported monetary input",
        "Confirm the exact positive amount, currency and supported precision with the merchant.",
      );
    const scoped = data.transactions.filter(
      (tx) => tx.merchant === ticket.merchant,
    );
    const refs = confirmedReference
      ? [confirmedReference.trim().toUpperCase()]
      : extracted.references;
    const matches = refs.length
      ? scoped.filter(
          (tx) => refs.includes(tx.id) || refs.includes(tx.reference),
        )
      : scoped.filter((tx) =>
          extracted.amounts.some(
            (a) => a.minor === tx.amountMinor && a.currency === tx.currency,
          ),
        );
    if (
      matches.some(
        (tx) =>
          !Number.isSafeInteger(tx.amountMinor) ||
          tx.amountMinor <= 0 ||
          !["EUR", "USD"].includes(tx.currency) ||
          ![
            "pending",
            "sent_to_bank",
            "credited",
            "failed",
            "returned",
          ].includes(tx.status) ||
          !tx.fetchedAt ||
          !tx.eventAt ||
          !Number.isFinite(Date.parse(tx.fetchedAt)) ||
          !Number.isFinite(Date.parse(tx.eventAt)) ||
          !/^LED-[A-Z0-9-]+$/.test(tx.ledger) ||
          !/^CLE-[A-Z0-9-]+$/.test(tx.clearing),
      )
    )
      return block(
        "Invalid source schema",
        "A required source field is missing or malformed. Use manual investigation.",
      );
    base.candidates = matches.map((tx) => ({ ...tx }));
    base.sources = matches.flatMap(sourceRecords);
    if (!matches.length)
      return block(
        refs.length
          ? "Reference unavailable in this account"
          : "Payment reference needed",
        "Ask the merchant for a unique reference and verify the currency. Do not infer ownership of an unavailable reference.",
      );
    if (matches.length !== 1 || !refs.length)
      return block(
        "A unique payment reference is needed",
        "An amount alone cannot confirm a transaction. Record the reference supplied by the merchant, or hand over with the authorized candidates.",
      );
    const tx = matches[0];
    if (refs.some((ref) => ref !== tx.id && ref !== tx.reference))
      return block(
        "Conflicting transaction references",
        "The request contains references that do not identify the same authorized payment. Clarify the merchant’s reference before drafting.",
      );
    if (
      extracted.amounts.length &&
      !extracted.amounts.every(
        (a) =>
          a.currency === tx.currency &&
          [tx.amountMinor, tx.netMinor].includes(a.minor),
      )
    )
      return block(
        "Amount or currency mismatch",
        "The request does not match this transaction. No silent FX conversion or amount-only match is allowed.",
      );
    const age = Date.parse(ticket.receivedAt) - Date.parse(tx.fetchedAt);
    if (!Number.isFinite(age) || age < 0 || age > 300000)
      return block(
        "Source snapshot needs refreshing",
        "The fixture snapshot is missing, in the future or older than five minutes at request time. Return to a person; reopening does not make data fresh.",
      );
    if (tx.clearingStatus && tx.clearingStatus !== tx.status)
      return block(
        "Conflicting source records",
        "The ledger and clearing record disagree. Both are available for investigation; no definitive status draft is generated.",
      );
    if (
      tx.feeMinor !== undefined &&
      (!Number.isSafeInteger(tx.feeMinor) ||
        tx.feeMinor < 0 ||
        !Number.isSafeInteger(tx.netMinor) ||
        tx.netMinor <= 0 ||
        tx.amountMinor - tx.feeMinor !== tx.netMinor)
    )
      return block(
        "Fee reconciliation failed",
        "The documented gross, fee and net do not reconcile.",
      );
    base.transaction = tx;
    base.state = "draft_ready";
    base.gate = "Unique reference · merchant and payment verified";
    base.checks = [
      "Merchant scope",
      "Unique reference",
      "Amount and currency",
      "Snapshot freshness",
      "Consistent status",
      "Evidence citations",
    ];
    base.draft = makeDraft(ticket, tx);
    // A generated reply passes the same rule gate used for edited suggestions.
    const gate = evaluateDraft(base, base.draft);
    if (!gate.passed)
      return block(
        "Reply checks failed",
        "Generated wording did not pass deterministic checks.",
      );
    return base;
  }
  function evaluateDraft(analysis, text) {
    const issues = [];
    if (!analysis.transaction || analysis.state !== "draft_ready")
      return {
        passed: false,
        critical: true,
        issues: ["No verified, answerable transaction."],
      };
    const tx = analysis.transaction,
      n = normalize(text);
    if (!text.trim()) issues.push("Reply is empty.");
    if (sanitizeInput(text).flagged)
      issues.push("Sensitive input must be removed before reply preparation.");
    if (
      /\b(guarantee|guaranteed|garanti|garantiert)\b|(?:arrive|credited|paid|refund|settle).{0,25}(?:tomorrow|today|within|by \d)|(?:demain|morgen).{0,25}(?:credit|gutgeschr|erstatt)|(?:released|refunded|transferred).{0,15}(?:funds|money)/i.test(
        text,
      )
    )
      issues.push("Unsupported promise or financial action.");
    const financial = entities(text);
    if (
      financial.amounts.some(
        (a) =>
          a.currency !== tx.currency ||
          ![tx.amountMinor, tx.feeMinor, tx.netMinor].includes(a.minor),
      )
    )
      issues.push("Amount or currency is not supported by the matched source.");
    if (financial.references.some((r) => r !== tx.reference && r !== tx.id))
      issues.push("Reference is not supported by the matched transaction.");
    const ids = [...text.matchAll(/\b(?:LED|CLE)-[A-Z0-9-]+\b/g)].map(
      (m) => m[0],
    );
    if (
      ids.some((id) => ![tx.ledger, tx.clearing].includes(id)) ||
      ![tx.ledger, tx.clearing].every((id) => ids.includes(id))
    )
      issues.push("Missing or invalid transaction citations.");
    if (
      tx.status !== "credited" &&
      /\b(definitely paid|has been credited|was credited|est credite|wurde gutgeschrieben)\b/.test(
        n,
      )
    )
      issues.push("The reply upgrades the recorded payment status.");
    const canonical = makeDraft(
      {
        language: /^Votre/.test(text) ? "FR" : /^Ihre/.test(text) ? "DE" : "EN",
      },
      tx,
    );
    const exact =
      text.replace(/\s+/g, " ").trim() ===
      canonical.replace(/\s+/g, " ").trim();
    const critical = issues.length > 0;
    if (!critical && !exact)
      issues.push(
        "Edited wording needs a manual factual review; the rules cannot certify free text.",
      );
    return { passed: issues.length === 0, critical, issues };
  }
  function handover(ticket, analysis, reason, note) {
    if (!reason.trim() || (reason === "Other — see agent note" && !note.trim()))
      throw new Error("A reason and, for Other, an agent note are required.");
    return {
      ticket: ticket.id,
      merchant: ticket.merchant,
      queue: analysis.queue,
      reason,
      note: sanitizeInput(note.trim()).text,
      gate: analysis.gate,
      sources: analysis.sources.map((s) => ({
        id: s.id,
        fetchedAt: s.fetchedAt,
      })),
      policy: "FLOW-POL-1",
      demo: true,
    };
  }
  globalThis.FlowEngine = {
    money,
    stamp,
    parseMinor,
    entities,
    sanitizeInput,
    classify,
    analyze,
    evaluateDraft,
    handover,
  };
})();
