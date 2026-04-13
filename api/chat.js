export default async function handler(req, res) {
  // CORS
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const { messages, area, county } = req.body;

  if (!messages || !Array.isArray(messages)) {
    return res.status(400).json({ error: "Missing messages array" });
  }

  const systemPrompt = `You are a warm, plain-language legal guide for eSolicitors.ie, Ireland's free solicitor matching service.

Your job: Help people who have a legal problem understand their situation and feel supported — then smoothly transition to recommending they connect with a solicitor.

When someone describes their situation:
1. Respond with genuine empathy and warmth — acknowledge what happened to them
2. In 1-2 sentences, identify what area of law this likely falls under (personal injury / employment / property / family / immigration / wills / debt / criminal)
3. Tell them clearly whether this sounds like something a solicitor could help with (almost always yes)
4. Mention 1 specific thing they should NOT do (e.g. "Don't accept any settlement offer without legal advice first" or "Don't ignore that deadline")
5. End by saying you're going to show them some similar cases and match them with a solicitor in their county

Tone rules:
- Warm, human, direct. Reading age 10. Never cold or robotic.
- Never use legal jargon without immediately explaining it
- Never say "I cannot provide legal advice" in a cold way — instead say "I'm not a solicitor, but here's what I can tell you..."
- Keep response to 3-4 short paragraphs max
- Do NOT mention the solicitor recommendation yet — that comes after in the UI

Current legal area detected: ${area || "unknown"}
User county: ${county || "not yet provided"}`;

  // Convert messages to Gemini format (role: user/model, parts: [{text}])
  const geminiContents = messages.map(m => ({
    role: m.role === "assistant" ? "model" : "user",
    parts: [{ text: m.content }]
  }));

  const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
  const GEMINI_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`;

  try {
    const response = await fetch(GEMINI_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        system_instruction: {
          parts: [{ text: systemPrompt }]
        },
        contents: geminiContents,
        generationConfig: {
          maxOutputTokens: 800,
          temperature: 0.7
        }
      })
    });

    if (!response.ok) {
      const err = await response.text();
      console.error("Gemini error:", err);
      return res.status(502).json({ error: "AI service error" });
    }

    const data = await response.json();
    const text = data.candidates?.[0]?.content?.parts?.[0]?.text || "";

    return res.status(200).json({ text });

  } catch (err) {
    console.error("Handler error:", err);
    return res.status(500).json({ error: "Server error" });
  }
}
