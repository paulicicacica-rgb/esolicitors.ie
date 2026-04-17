export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const url = process.env.UPSTASH_REDIS_URL;
  const token = process.env.UPSTASH_REDIS_TOKEN;
  if (!url || !token) return res.status(500).json({ error: 'Redis not configured' });

  try {
    const { name, phone, county, issue, transcript, source } = req.body;

    const lead = {
      id: `lead_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
      date: new Date().toISOString(),
      name: name || '',
      phone: phone || '',
      county: county || '',
      issue: issue || '',
      transcript: transcript || '',
      source: source || '/'
    };

    const headers = {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    };

    await fetch(`${url}/set/lead:${lead.id}`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ value: JSON.stringify(lead) })
    });

    await fetch(`${url}/zadd/leads_index`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ value: [Date.now(), lead.id] })
    });

    return res.status(200).json({ ok: true, id: lead.id });

  } catch (err) {
    console.error('Lead save error:', err);
    return res.status(500).json({ ok: false, error: err.message });
  }
}
