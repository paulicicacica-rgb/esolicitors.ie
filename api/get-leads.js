export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');

  const url = process.env.UPSTASH_REDIS_URL;
  const token = process.env.UPSTASH_REDIS_TOKEN;
  if (!url || !token) return res.status(500).json({ error: 'Redis not configured' });

  try {
    const headers = { Authorization: 'Bearer ' + token };

    // Get all keys matching lead:* pattern
    const keysRes = await fetch(url + '/keys/lead:*', { headers });
    const keysData = await keysRes.json();
    const keys = keysData.result || [];

    if (keys.length === 0) return res.status(200).json({ leads: [], total: 0 });

    // Fetch all leads in parallel
    const leads = await Promise.all(
      keys.map(async (key) => {
        try {
          const r = await fetch(url + '/get/' + key, { headers });
          const d = await r.json();
          if (!d.result) return null;
          // Handle both formats: plain JSON string or wrapped {"value":"..."}
          let parsed;
          try {
            parsed = JSON.parse(d.result);
            // If it has a "value" wrapper, unwrap it
            if (parsed && parsed.value && typeof parsed.value === 'string') {
              parsed = JSON.parse(parsed.value);
            }
          } catch {
            return null;
          }
          return parsed;
        } catch {
          return null;
        }
      })
    );

    // Filter nulls and sort newest first
    const filtered = leads
      .filter(Boolean)
      .sort((a, b) => new Date(b.date) - new Date(a.date));

    return res.status(200).json({ leads: filtered, total: filtered.length });

  } catch (err) {
    console.error('Get leads error:', err);
    return res.status(500).json({ ok: false, error: err.message });
  }
}
