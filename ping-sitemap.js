// ping-sitemap.js
// Run after deploy to notify Google of updated sitemap
// Usage: node ping-sitemap.js

const SITEMAPS = [
  "https://esolicitors.ie/sitemap.xml",
];

async function pingSitemap(url) {
  const pingUrl = `https://www.google.com/ping?sitemap=${encodeURIComponent(url)}`;
  try {
    const res = await fetch(pingUrl);
    console.log(`✅ Pinged: ${url} → ${res.status}`);
  } catch (err) {
    console.error(`❌ Failed: ${url} → ${err.message}`);
  }
}

(async () => {
  console.log("🚀 Pinging sitemaps...");
  for (const sitemap of SITEMAPS) {
    await pingSitemap(sitemap);
  }
  console.log("Done.");
})();
