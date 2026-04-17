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
    const id = 'lead_' + Date.now() + '_' + Math.random().toString(36).slice(2, 7);

    const lead = {
      id,
      date: new Date().toISOString(),
      name: name || '',
      phone: phone || '',
      county: county || '',
      issue: issue || '',
      transcript: transcript || '',
      source: source || '/'
    };

    const headers = {
      Authorization: 'Bearer ' + token,
      'Content-Type': 'application/json'
    };

    // Save lead data as string
    await fetch(url + '/set/lead:' + id, {
      method: 'POST',
      headers,
      body: JSON.stringify([JSON.stringify(lead)])
    });

    // Add to sorted set — correct Upstash REST format: [score, member]
    const score = Date.now();
    await fetch(url + '/zadd/leads_index/' + score + '/' + id, {
      method: 'POST',
      headers
    });

    return res.status(200).json({ ok: true, id });

  } catch (err) {
    console.error('Lead save error:', err);
    return res.status(500).json({ ok: false, error: err.message });
  }
}
