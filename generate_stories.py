import json
import os
import re
import time
import urllib.request
import urllib.error

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    raise Exception("ANTHROPIC_API_KEY not set")

with open("stories_data.json", "r") as f:
    data = json.load(f)

SYSTEM_PROMPT = """You are writing SEO-optimised HTML pages for eSolicitors.ie, an Irish solicitor matching service.

Write a complete, self-contained HTML page for a personal injury story. The page should:
- Be written in plain, warm, direct English — no legal jargon
- Feel like a real person's story, not a press release
- Include the relevant Irish law explained simply
- Include what compensation typically looks like
- Include a warning about time limits
- End with Sarah's chat widget already in the HTML

Output ONLY valid HTML. No markdown. No explanation. No backticks.

The HTML must follow this exact structure:
1. Full <!DOCTYPE html> with head, meta, title, styles
2. Nav with eSolicitors.ie branding
3. Breadcrumb
4. Hero section with the person's name, location and situation as h1
5. Main story section — expand the situation into 4-5 paragraphs telling the full story naturally
6. What the law says section — explain the relevant law simply
7. What they were entitled to section — compensation explained plainly
8. Warning box — time limits
9. Similar cases section — 3 short made-up similar cases (different names/locations)
10. Sarah chat section: <div style="background:var(--cream-dark);padding:0 5%"><div style="max-width:540px;margin:0 auto;padding:40px 0"><script src="/sarah.js" data-mode="inline"></script></div></div>
11. Footer with eSolicitors.ie links

Use these CSS variables: --navy:#0c1f3d --gold:#c8922a --cream:#f7f3ee --cream-dark:#ede7dc --white:#fff --text-mid:#4a5568

The page title and h1 should target a long-tail search query based on the story situation.
Include a <meta name="description"> that reads like a human wrote it.
"""

def call_claude(prompt):
    payload = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 4000,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}]
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
            return result["content"][0]["text"]
    except urllib.error.HTTPError as e:
        print(f"    API error {e.code}: {e.read().decode()}")
        return None

generated = 0
skipped = 0

for subcat in data["subcategories"]:
    for story in subcat["stories"]:
        folder = f"./{data['practice_area']}/{subcat['slug']}/{story['slug']}"
        filepath = f"{folder}/index.html"

        if os.path.exists(filepath):
            print(f"  SKIP (exists): {filepath}")
            skipped += 1
            continue

        print(f"  Generating: {filepath}")

        prompt = f"""Generate a full story page for eSolicitors.ie with these details:

Person: {story['name']} from {story['location']}
Subcategory: {subcat['label']}
Situation: {story['situation']}
Outcome: {story['outcome']}
Hub page URL: {subcat['hub_url']}
Relevant law: {subcat['law']}
Time limit: {subcat['time_limit']}
Compensation range: {subcat['compensation_range']}
Practice area: {data['practice_area_label']}

Breadcrumb path: Home > Personal Injury > {subcat['label']} > {story['name']}'s Story

The page URL will be: /personal-injury/{subcat['slug']}/{story['slug']}/
"""

        html = call_claude(prompt)

        if html:
            os.makedirs(folder, exist_ok=True)
            # Clean up any accidental markdown fences
            html = re.sub(r"^```html\s*", "", html.strip())
            html = re.sub(r"\s*```$", "", html.strip())
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"    Saved: {filepath}")
            generated += 1
            time.sleep(0.5)  # avoid rate limiting
        else:
            print(f"    FAILED: {filepath}")

        time.sleep(0.3)

print(f"\nDone. Generated: {generated}, Skipped: {skipped}")
