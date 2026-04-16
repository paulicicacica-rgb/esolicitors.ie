export default async function handler(req, res) {
  const url = process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.UPSTASH_REDIS_REST_TOKEN;

  if (!url || !token) {
    return res.status(500).json({
      ok: false,
      error: "Missing env vars",
      url: !!url,
      token: !!token
    });
  }

  try {
    // Write a test value
    const setRes = await fetch(`${url}/set/test-key/hello-esolicitors`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const setData = await setRes.json();

    // Read it back
    const getRes = await fetch(`${url}/get/test-key`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const getData = await getRes.json();

    return res.status(200).json({
      ok: true,
      write: setData,
      read: getData,
      message: getData.result === "hello-esolicitors" ? "Upstash working!" : "Something off"
    });

  } catch (err) {
    return res.status(500).json({ ok: false, error: err.message });
  }
}
