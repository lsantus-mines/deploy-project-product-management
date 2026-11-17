/* Client for the FlowAssist API (api/index.py).

   The browser engine gives an instant preview; the server decides every
   recorded action. Product events go to the same server (POST /api/events),
   which keeps them locally (metrics/events.jsonl with `make dev`, runtime logs
   on Vercel): no third-party analytics, no ticket, draft or note text.
   Opened from file:// there is no server: the page runs in local preview
   mode and says so. */
(() => {
  "use strict";
  const enabled =
    typeof location !== "undefined" && /^https?:$/.test(location.protocol);
  const sessionId = `ops-${Math.random().toString(36).slice(2, 10)}`;

  async function request(method, path, body) {
    const response = await fetch(`/api/${path}`, {
      method,
      headers: { "content-type": "application/json", "x-session-id": sessionId },
      body: body ? JSON.stringify(body) : undefined,
    });
    const data = await response.json().catch(() => ({}));
    return { status: response.status, data };
  }

  globalThis.FlowServer = {
    enabled,
    sessionId,
    async config() {
      const result = await request("GET", "config");
      if (result.status !== 200) throw new Error(`config ${result.status}`);
      return result.data;
    },
    analyze: (body) => request("POST", "analyze", body),
    check: (body) => request("POST", "check", body),
    handover: (body) => request("POST", "handover", body),
    track(event, properties = {}) {
      if (!enabled) return;
      // Fire and forget: metrics must never block or break the workflow.
      fetch("/api/events", {
        method: "POST",
        keepalive: true,
        headers: { "content-type": "application/json", "x-session-id": sessionId },
        body: JSON.stringify({ event, properties }),
      }).catch(() => {});
    },
  };
})();
