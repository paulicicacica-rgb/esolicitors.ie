export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');

  const webhook = process.env.GOOGLE_SHEETS_WEBHOOK;
  if (!webhook) return res.status(500).json({ error: 'Webhook not configured' });

  try {
    // Google Sheets read via Apps Script GET endpoint
    const sheetId = process.env.GOOGLE_SHEET_ID;
    const apiKey = process.env.GOOGLE_API_KEY;

    if (!sheetId || !apiKey) {
      // Fallback: return empty leads with helpful message
      return res.status(200).json({
        leads: [],
        message: 'Add GOOGLE_SHEET_ID and GOOGLE_API_KEY to env vars to read leads'
      });
    }

    const url = `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/Sheet1?key=${apiKey}`;
    const response = await fetch(url);
    const data = await response.json();

    if (!data.values || data.values.length < 2) {
      return res.status(200).json({ leads: [] });
    }

    const [headers, ...rows] = data.values;

    const leads = rows.map((row, i) => ({
      id: `lead_${i}_${row[0] || i}`,
      date: row[0] || '',
      name: row[1] || '',
      phone: row[2] || '',
      county: row[3] || '',
      issue: row[4] || '',
      transcript: row[5] || '',
      source: row[6] || ''
    })).reverse(); // newest first

    return res.status(200).json({ leads });

  } catch (err) {
    console.error('Get leads error:', err);
    return res.status(500).json({ ok: false, error: err.message });
  }
}
