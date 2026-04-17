export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  const { messages, system, area, county } = req.body;

  if (!messages || !Array.isArray(messages)) {
    return res.status(400).json({ error: 'Invalid request body' });
  }

  // Support both old format (area/county) and new format (system)
  let systemPrompt = system || '';
  if (!systemPrompt && area) {
    systemPrompt = `You are a warm plain-language legal guide on eSolicitors.ie. The person is on the ${area} page${county ? ' in ' + county : ''}. Listen to their situation with empathy. Assess whether it sounds like a valid claim under Irish law. Give a realistic sense of their options. Tell them one important thing to do or not do. Recommend they connect with a solicitor — warm not pushy. Tone: warm, human, direct. Reading age 10. Keep responses to 3 short paragraphs.`;
  }

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 1000,
        system: systemPrompt,
        messages,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      console.error('Anthropic error:', data);
      return res.status(response.status).json({ error: data.error?.message || 'API error' });
    }

    // Support both old format (data.text) and new format (data.content)
    const text = data.content?.[0]?.text || '';
    return res.status(200).json({ ...data, text });

  } catch (err) {
    console.error('Server error:', err);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
