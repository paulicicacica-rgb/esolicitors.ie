import glob
import re
import os
import json
import time
import urllib.request
import urllib.error

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    raise Exception("ANTHROPIC_API_KEY not set")

SYSTEM = """You write concise, high-converting SEO meta titles and descriptions for an Irish legal website called eSolicitors.ie.

Rules:
- Title: 50-60 characters max. Include the main keyword + Ireland + eSolicitors.ie
- Description: 140-155 characters max. Plain English. Include a clear benefit and mild urgency. No emojis.
- Sound human, not robotic
- Target Irish searchers looking for legal help
- Never mention fees or prices

Respond ONLY with valid JSON, no markdown:
{"title": "...", "description": "..."}"""

def call_claude(page_context):
    payload = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 200,
        "system": SYSTEM,
        "messages": [{"role": "user", "content": f"Write meta title and description for this page:\n\n{page_context}"}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        print(f"    API error {e.code}: {e.read().decode()[:100]}")
        return None

def extract_context(content, filepath):
    """Extract page context for Claude to write good meta tags"""
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    h1 = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else ''

    title = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title.group(1).strip() if title else ''

    # Get first paragraph of body text
    body_text = re.findall(r'<p[^>]*>([^<]{30,})</p>', content)
    first_para = body_text[0][:200] if body_text else ''

    path = filepath.replace('./', '').replace('/index.html', '').replace('.html', '')

    return f"URL path: /{path}\nCurrent title: {title}\nH1: {h1}\nFirst paragraph: {first_para}"

def already_has_good_meta(content):
    """Skip pages that already have decent meta tags"""
    title = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)

    if not title or not desc:
        return False

    t = title.group(1).strip()
    d = desc.group(1).strip()

    # Skip if title looks good (has esolicitors or .ie and is reasonable length)
    if len(t) > 30 and ('eSolicitors' in t or 'Ireland' in t or 'Irish' in t):
        if len(d) > 80:
            return True
    return False

files = sorted(set(
    glob.glob("./**/*.html", recursive=True) +
    glob.glob("./*.html")
))

updated = 0
skipped = 0

for filepath in files:
    if any(x in filepath for x in ['.github', '/api/']):
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    if already_has_good_meta(content):
        skipped += 1
        continue

    print(f"  Processing: {filepath}")

    context = extract_context(content, filepath)
    raw = call_claude(context)

    if not raw:
        print(f"    FAILED")
        continue

    try:
        clean = raw.replace('```json', '').replace('```', '').strip()
        match = re.search(r'\{[\s\S]*\}', clean)
        parsed = json.loads(match.group(0)) if match else None
        if not parsed or not parsed.get('title') or not parsed.get('description'):
            raise ValueError("Missing fields")
    except Exception as e:
        print(f"    Parse error: {e}")
        continue

    title = parsed['title']
    desc = parsed['description']

    # Update or insert title
    if re.search(r'<title>.*?</title>', content, re.IGNORECASE):
        content = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', content, flags=re.IGNORECASE)
    else:
        content = content.replace('<head>', f'<head>\n<title>{title}</title>', 1)

    # Update or insert meta description
    if re.search(r'<meta\s+name=["\']description["\']', content, re.IGNORECASE):
        content = re.sub(
            r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\'][^>]*/?>',
            f'<meta name="description" content="{desc}">',
            content,
            flags=re.IGNORECASE
        )
    else:
        content = content.replace('</title>', f'</title>\n<meta name="description" content="{desc}">', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"    Title: {title}")
    updated += 1
    time.sleep(0.3)

print(f"\nDone. Updated: {updated}, Skipped (already good): {skipped}")
