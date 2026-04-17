export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');

  const url = process.env.UPSTASH_REDIS_URL;
  const token = process.env.UPSTASH_REDIS_TOKEN;
  if (!url || !token) return res.status(500).json({ error: 'Redis not configured' });

  try {
    const headers = { Authorization: `Bearer ${token}` };

    const indexRes = await fetch(`${url}/zrange/leads_index/0/-1/rev`, { headers });
    const indexData = await indexRes.json();
    const ids = indexData.result || [];

    if (ids.length === 0) return res.status(200).json({ leads: [], total: 0 });

    const leads = await Promise.all(
      ids.map(async (id) => {
        try {
          const r = await fetch(`${url}/get/lead:${id}`, { headers });
          const d = await r.json();
          return d.result ? JSON.parse(d.result) : null;
        } catch {
          return null;
        }
      })
    );

    const filtered = leads.filter(Boolean);
    return res.status(200).json({ leads: filtered, total: filtered.length });

  } catch (err) {
    console.error('Get leads error:', err);
    return res.status(500).json({ ok: false, error: err.message });
  }
}
