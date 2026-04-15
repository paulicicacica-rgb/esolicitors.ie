/**
 * sarah.js — eSolicitors.ie chat widget
 * Usage: <script src="/sarah.js"></script>
 * Embeds inline chat at bottom of page OR as floating bubble.
 * Mode: set data-mode="inline" or data-mode="float" on the script tag.
 * Default: inline
 */

(function () {
  const scriptTag = document.currentScript;
  const rawMode = (scriptTag && scriptTag.getAttribute("data-mode")) || "inline";
  const mode = rawMode === "inline-hero" ? "inline" : rawMode;

  const SARAH_AVATAR =
    "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face";

  const SOLICITOR_PROFILES = [
    { name: "Ciara O'Brien", area: "Criminal & Road Traffic Law", county: "Dublin", reviews: 47, rating: "5.0", img: "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=80&h=80&fit=crop&crop=face" },
    { name: "Michael Fitzgerald", area: "Drink Driving Defence", county: "Cork", reviews: 31, rating: "4.9", img: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&h=80&fit=crop&crop=face" },
    { name: "Sinead Gallagher", area: "Road Traffic Offences", county: "Galway", reviews: 28, rating: "5.0", img: "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=80&h=80&fit=crop&crop=face" },
  ];

  const SYSTEM_PROMPT = `You are Sarah, a warm and caring intake assistant for eSolicitors.ie, an Irish solicitor matching service. You are kind, human, and make people feel immediately at ease.

STAGE: story
- The user has just described their situation.
- Respond with genuine warmth and empathy (2-3 sentences). Do NOT give legal advice.
- Say something like: "You are in the right place. Whatever has happened, the most important thing right now is getting a good solicitor on your side — and that is exactly what we are here for. Why don't you leave me your name and number and one of our solicitors will be in touch with you shortly."
- Ask: "Can I start with your first name?"
- Set next_stage to: name
- Set show_solicitors to: true

STAGE: name
- User gave their name. Use it warmly.
- Ask: "Thank you. And what is the best number for a solicitor to reach you on?"
- Set next_stage to: phone

STAGE: phone
- User gave their phone number.
- Respond warmly. Say: "Perfect. One of our solicitors will be in touch with you shortly — usually within a few hours. You are in good hands."
- Set next_stage to: done

STAGE: done
- Respond briefly and reassuringly if the user says anything else.

RULES:
- You are Sarah. Always warm, never robotic.
- Never give legal advice. Never mention fees.
- 2-4 sentences max per reply.
- No emojis. No slang. Plain warm English.
- Respond ONLY with valid JSON, no markdown, no backticks:
{"message": "your response", "next_stage": "name|phone|done", "show_solicitors": true|false}
show_solicitors is true ONLY for the first reply to the user's story.`;

  // ── Styles ──────────────────────────────────────────────────────────────────

  const css = `
    :root {
      --es-navy: #0f1e35;
      --es-navy-mid: #1a2f4a;
      --es-gold: #b8975a;
      --es-cream: #f7f4ef;
      --es-text: #1c1c1c;
      --es-soft: #5a5a5a;
      --es-border: #e2ddd6;
      --es-white: #ffffff;
    }

    /* ── INLINE MODE ── */
    #es-inline-wrap {
      font-family: 'DM Sans', 'Segoe UI', sans-serif;
      width: 100%;
      max-width: 540px;
      margin: 48px auto;
      background: var(--es-white);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 8px 40px rgba(15,30,53,0.11);
      display: flex;
      flex-direction: column;
      height: 560px;
    }

    /* ── FLOAT MODE ── */
    #es-float-btn {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: var(--es-navy);
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(15,30,53,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9998;
      transition: transform 0.2s;
    }
    #es-float-btn:hover { transform: scale(1.07); }
    #es-float-btn img {
      width: 44px; height: 44px;
      border-radius: 50%;
      object-fit: cover;
      border: 2px solid var(--es-gold);
    }
    #es-float-badge {
      position: absolute;
      top: 0; right: 0;
      width: 14px; height: 14px;
      background: #4ade80;
      border-radius: 50%;
      border: 2px solid white;
    }
    #es-float-panel {
      position: fixed;
      bottom: 96px;
      right: 24px;
      width: 360px;
      max-width: calc(100vw - 48px);
      height: 520px;
      background: var(--es-white);
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 8px 40px rgba(15,30,53,0.18);
      display: flex;
      flex-direction: column;
      z-index: 9997;
      transform: scale(0.92) translateY(16px);
      opacity: 0;
      pointer-events: none;
      transition: transform 0.25s ease, opacity 0.25s ease;
      font-family: 'DM Sans', 'Segoe UI', sans-serif;
    }
    #es-float-panel.open {
      transform: scale(1) translateY(0);
      opacity: 1;
      pointer-events: all;
    }

    /* ── SHARED ── */
    .es-header {
      background: var(--es-navy);
      padding: 16px 18px;
      display: flex;
      align-items: center;
      gap: 12px;
      position: relative;
      flex-shrink: 0;
    }
    .es-header-avatar {
      width: 42px; height: 42px;
      border-radius: 50%;
      overflow: hidden;
      border: 2px solid var(--es-gold);
      flex-shrink: 0;
    }
    .es-header-avatar img { width: 100%; height: 100%; object-fit: cover; }
    .es-header-text h3 {
      font-size: 15px;
      font-weight: 600;
      color: var(--es-white);
      margin: 0;
      letter-spacing: 0.01em;
    }
    .es-header-text p {
      font-size: 11px;
      color: rgba(255,255,255,0.5);
      margin: 2px 0 0;
      font-weight: 300;
    }
    .es-status {
      width: 9px; height: 9px;
      background: #4ade80;
      border-radius: 50%;
      position: absolute;
      right: 18px; top: 50%;
      transform: translateY(-50%);
      animation: es-pulse 2s infinite;
    }
    @keyframes es-pulse {
      0%,100% { box-shadow: 0 0 0 2px rgba(74,222,128,0.25); }
      50% { box-shadow: 0 0 0 6px rgba(74,222,128,0.08); }
    }

    .es-messages {
      flex: 1;
      overflow-y: auto;
      padding: 18px 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      scroll-behavior: smooth;
    }
    .es-messages::-webkit-scrollbar { width: 3px; }
    .es-messages::-webkit-scrollbar-thumb { background: var(--es-border); border-radius: 2px; }

    .es-row {
      display: flex;
      align-items: flex-end;
      gap: 7px;
      animation: es-up 0.3s ease;
    }
    .es-row.es-user { flex-direction: row-reverse; }
    @keyframes es-up {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .es-av {
      width: 28px; height: 28px;
      border-radius: 50%;
      overflow: hidden;
      flex-shrink: 0;
      border: 1.5px solid var(--es-gold);
    }
    .es-av img { width: 100%; height: 100%; object-fit: cover; }

    .es-bubble {
      max-width: 78%;
      padding: 10px 13px;
      border-radius: 14px;
      font-size: 13.5px;
      line-height: 1.6;
    }
    .es-bubble.es-ai { background: #f0ede8; color: var(--es-text); border-bottom-left-radius: 3px; }
    .es-bubble.es-user { background: var(--es-navy); color: var(--es-white); border-bottom-right-radius: 3px; }

    .es-sol-cards {
      display: flex;
      flex-direction: column;
      gap: 7px;
      padding-left: 35px;
      animation: es-up 0.4s ease;
    }
    .es-sol-card {
      background: var(--es-white);
      border: 1px solid var(--es-border);
      border-radius: 10px;
      padding: 9px 11px;
      display: flex;
      align-items: center;
      gap: 9px;
      box-shadow: 0 2px 8px rgba(15,30,53,0.06);
    }
    .es-sol-av {
      width: 36px; height: 36px;
      border-radius: 50%;
      overflow: hidden;
      flex-shrink: 0;
      border: 1.5px solid var(--es-border);
    }
    .es-sol-av img { width: 100%; height: 100%; object-fit: cover; }
    .es-sol-info { flex: 1; min-width: 0; }
    .es-sol-name { font-size: 12.5px; font-weight: 500; color: var(--es-text); }
    .es-sol-area { font-size: 10.5px; color: var(--es-soft); margin-top: 1px; }
    .es-sol-stars { color: #f5a623; font-size: 10px; margin-top: 2px; }
    .es-sol-badge {
      background: var(--es-navy);
      color: var(--es-white);
      font-size: 8.5px;
      font-weight: 500;
      border-radius: 4px;
      padding: 3px 6px;
      white-space: nowrap;
      flex-shrink: 0;
    }

    .es-typing {
      display: flex;
      align-items: flex-end;
      gap: 7px;
      animation: es-up 0.3s ease;
    }
    .es-typing-bubble {
      background: #f0ede8;
      border-radius: 14px;
      border-bottom-left-radius: 3px;
      padding: 11px 14px;
      display: flex;
      gap: 4px;
      align-items: center;
    }
    .es-dot {
      width: 5px; height: 5px;
      background: #bbb;
      border-radius: 50%;
      animation: es-bounce 1.2s infinite;
    }
    .es-dot:nth-child(2) { animation-delay: 0.2s; }
    .es-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes es-bounce {
      0%,60%,100% { transform: translateY(0); }
      30% { transform: translateY(-4px); }
    }

    .es-input-wrap {
      border-top: 1px solid var(--es-border);
      padding: 12px 14px;
      background: var(--es-white);
      flex-shrink: 0;
    }
    .es-input-row {
      display: flex;
      align-items: center;
      gap: 9px;
      background: var(--es-cream);
      border: 1px solid var(--es-border);
      border-radius: 11px;
      padding: 9px 12px;
      transition: border-color 0.2s;
    }
    .es-input-row:focus-within { border-color: var(--es-gold); }
    .es-input-row textarea {
      flex: 1;
      border: none;
      background: transparent;
      font-family: inherit;
      font-size: 13px;
      color: var(--es-text);
      resize: none;
      outline: none;
      line-height: 1.5;
      max-height: 72px;
      overflow-y: auto;
    }
    .es-input-row textarea::placeholder { color: #bbb; }
    .es-send {
      width: 34px; height: 34px;
      border-radius: 8px;
      background: var(--es-navy);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: background 0.2s, transform 0.1s;
    }
    .es-send:hover { background: var(--es-navy-mid); }
    .es-send:active { transform: scale(0.95); }
    .es-send svg { width: 14px; height: 14px; fill: none; stroke: white; stroke-width: 2; }
    .es-privacy {
      text-align: center;
      font-size: 10.5px;
      color: #bbb;
      margin-top: 7px;
    }
  `;

  // ── Inject styles ────────────────────────────────────────────────────────────

  const style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  // Load DM Sans if not already present
  if (!document.querySelector('link[href*="DM+Sans"]')) {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap";
    document.head.appendChild(link);
  }

  // ── Build HTML ───────────────────────────────────────────────────────────────

  function buildChatHTML(containerId, messagesId, inputId) {
    return `
      <div class="es-header">
        <div class="es-header-avatar"><img src="${SARAH_AVATAR}" alt="Sarah"/></div>
        <div class="es-header-text">
          <h3>Sarah — eSolicitors.ie</h3>
          <p>Legal intake assistant &middot; Here to help</p>
        </div>
        <div class="es-status"></div>
      </div>
      <div class="es-messages" id="${messagesId}">
        <div class="es-row">
          <div class="es-av"><img src="${SARAH_AVATAR}" alt="Sarah"/></div>
          <div class="es-bubble es-ai">
            Hi, I'm Sarah from eSolicitors.ie.<br><br>
            Whatever has brought you here today — tell me what happened and I will make sure you get to the right solicitor.
          </div>
        </div>
      </div>
      <div class="es-input-wrap">
        <div class="es-input-row">
          <textarea id="${inputId}" rows="1" placeholder="Tell me what happened..."></textarea>
          <button class="es-send" data-send="${containerId}">
            <svg viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          </button>
        </div>
        <div class="es-privacy">Your story is private and never shared without your consent</div>
      </div>
    `;
  }

  // ── State per instance ───────────────────────────────────────────────────────

  function createInstance(messagesId, inputId) {
    let history = [];
    let stage = "story";
    let collected = {};

    function addMsg(text, isUser) {
      const wrap = document.getElementById(messagesId);
      const row = document.createElement("div");
      row.className = "es-row" + (isUser ? " es-user" : "");
      if (!isUser) {
        const av = document.createElement("div");
        av.className = "es-av";
        av.innerHTML = `<img src="${SARAH_AVATAR}" alt="Sarah"/>`;
        row.appendChild(av);
      }
      const bubble = document.createElement("div");
      bubble.className = "es-bubble " + (isUser ? "es-user" : "es-ai");
      bubble.textContent = text;
      row.appendChild(bubble);
      wrap.appendChild(row);
      wrap.scrollTop = wrap.scrollHeight;
    }

    function showCards() {
      const wrap = document.getElementById(messagesId);
      const cards = document.createElement("div");
      cards.className = "es-sol-cards";
      SOLICITOR_PROFILES.forEach(sol => {
        const card = document.createElement("div");
        card.className = "es-sol-card";
        card.innerHTML = `
          <div class="es-sol-av"><img src="${sol.img}" alt="${sol.name}"/></div>
          <div class="es-sol-info">
            <div class="es-sol-name">${sol.name}</div>
            <div class="es-sol-area">${sol.area} &middot; ${sol.county}</div>
            <div class="es-sol-stars">★★★★★ <span style="color:#999;font-size:9px">${sol.rating} (${sol.reviews} reviews)</span></div>
          </div>
          <div class="es-sol-badge">Verified</div>`;
        cards.appendChild(card);
      });
      wrap.appendChild(cards);
      wrap.scrollTop = wrap.scrollHeight;
    }

    function showTyping() {
      const wrap = document.getElementById(messagesId);
      const row = document.createElement("div");
      row.className = "es-typing";
      row.id = messagesId + "-typing";
      row.innerHTML = `
        <div class="es-av"><img src="${SARAH_AVATAR}" alt="Sarah"/></div>
        <div class="es-typing-bubble">
          <div class="es-dot"></div><div class="es-dot"></div><div class="es-dot"></div>
        </div>`;
      wrap.appendChild(row);
      wrap.scrollTop = wrap.scrollHeight;
    }

    function removeTyping() {
      const t = document.getElementById(messagesId + "-typing");
      if (t) t.remove();
    }

    async function send() {
      const input = document.getElementById(inputId);
      const text = input.value.trim();
      if (!text) return;
      input.value = "";
      input.style.height = "auto";
      addMsg(text, true);
      history.push({ role: "user", content: text });
      if (stage === "name") collected.name = text;
      if (stage === "phone") collected.phone = text;
      showTyping();

      try {
        const res = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            system: SYSTEM_PROMPT + `\n\nCurrent stage: ${stage}`,
            messages: history
          })
        });

        if (!res.ok) {
          const e = await res.json().catch(() => ({}));
          removeTyping();
          addMsg("Error: " + (e.error || `HTTP ${res.status}`), false);
          return;
        }

        const data = await res.json();
        removeTyping();
        const raw = data.content?.[0]?.text || "";
        let parsed;
        try {
          const match = raw.replace(/```json|```/g, "").trim().match(/\{[\s\S]*\}/);
          parsed = match ? JSON.parse(match[0]) : null;
          if (!parsed || !parsed.message) throw new Error("no message");
        } catch {
          parsed = { message: raw || "Something went wrong.", next_stage: stage, show_solicitors: false };
        }

        addMsg(parsed.message, false);
        history.push({ role: "assistant", content: parsed.message });
        if (parsed.show_solicitors) setTimeout(showCards, 500);
        if (parsed.next_stage) stage = parsed.next_stage;
        if (stage === "done" && collected.phone) {
          console.log("eSolicitors lead:", collected);
          // TODO: POST to Google Sheets webhook
        }
      } catch (err) {
        removeTyping();
        addMsg("Network error: " + err.message, false);
      }
    }

    // Bind textarea resize + enter key
    const input = document.getElementById(inputId);
    if (input) {
      input.addEventListener("input", () => {
        input.style.height = "auto";
        input.style.height = Math.min(input.scrollHeight, 72) + "px";
      });
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
      });
    }

    return { send };
  }

  // ── Mount ────────────────────────────────────────────────────────────────────

  if (mode === "inline") {
    // Inject inline block before </body> or at script location
    const wrap = document.createElement("div");
    wrap.id = "es-inline-wrap";
    wrap.innerHTML = buildChatHTML("es-inline", "es-inline-msgs", "es-inline-input");
    scriptTag.parentNode.insertBefore(wrap, scriptTag);
    const instance = createInstance("es-inline-msgs", "es-inline-input");
    wrap.querySelector('[data-send="es-inline"]').addEventListener("click", instance.send);

  } else {
    // Float button + panel
    const btn = document.createElement("button");
    btn.id = "es-float-btn";
    btn.innerHTML = `<img src="${SARAH_AVATAR}" alt="Sarah"/><div id="es-float-badge"></div>`;
    document.body.appendChild(btn);

    const panel = document.createElement("div");
    panel.id = "es-float-panel";
    panel.innerHTML = buildChatHTML("es-float", "es-float-msgs", "es-float-input");
    document.body.appendChild(panel);

    const instance = createInstance("es-float-msgs", "es-float-input");
    panel.querySelector('[data-send="es-float"]').addEventListener("click", instance.send);

    btn.addEventListener("click", () => {
      panel.classList.toggle("open");
    });
  }
})();

// Patch: inline-hero mode — same as inline, mounts at script location
// Already handled by default inline logic since insertBefore(wrap, scriptTag) works anywhere
