import glob
import re
import os
import json
import time
import urllib.request
import urllib.error
import unicodedata

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    raise Exception("ANTHROPIC_API_KEY not set")

def slugify(text):
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    return text

def call_claude(system, prompt):
    payload = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 3000,
        "system": system,
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
            return result["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        print(f"    API error {e.code}: {e.read().decode()[:200]}")
        return None

SYSTEM = """You write short, human story pages for eSolicitors.ie — an Irish solicitor matching service.

Write a complete HTML page for a legal case story. Rules:
- Plain warm English, no jargon
- Tell the person's story naturally in 3-4 paragraphs
- One section: what the law says (simple, 1 paragraph)
- One warning box: time limits
- NO similar cases, NO contact info, NO phone numbers, NO office address, NO "our process", NO "why choose us"
- Stop after the time limit warning box — nothing more
- Use CSS variables: --navy:#0c1f3d --gold:#c8922a --cream:#f7f3ee --cream-dark:#ede7dc
- Include nav with eSolicitors.ie branding and breadcrumb
- Output ONLY valid HTML. No markdown. No backticks."""

CTA_FOOTER = """
<div style="background:var(--navy,#0c1f3d);padding:60px 5%;text-align:center">
  <div style="max-width:600px;margin:0 auto">
    <div style="font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold,#c8922a);margin-bottom:12px">Free Solicitor Matching</div>
    <h2 style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;color:#fff;margin-bottom:14px;line-height:1.2">Sound familiar?<br>You may have a case too.</h2>
    <p style="color:rgba(255,255,255,0.6);font-size:.95rem;margin-bottom:32px;line-height:1.7">Tell Sarah what happened. She will explain your options and match you with the right solicitor in your county — free.</p>
  </div>
  <div style="max-width:480px;margin:0 auto">
    <script src="/sarah.js" data-mode="inline"></script>
  </div>
</div>
<footer style="background:#080f1e;padding:36px 5%;font-family:'DM Sans',sans-serif">
  <div style="max-width:1100px;margin:0 auto">
    <div style="display:flex;flex-wrap:wrap;gap:32px;justify-content:space-between;margin-bottom:28px">
      <div>
        <a href="/" style="font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:#fff;text-decoration:none">e<span style="color:var(--gold,#c8922a)">Solicitors</span>.ie</a>
        <p style="font-size:.8rem;color:rgba(255,255,255,0.35);margin-top:8px;max-width:240px;line-height:1.6">Ireland's free solicitor matching service.</p>
      </div>
      <div style="display:flex;gap:40px;flex-wrap:wrap">
        <div>
          <h4 style="font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-bottom:12px">Navigate</h4>
          <ul style="list-style:none;display:flex;flex-direction:column;gap:8px">
            <li><a href="/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Home</a></li>
            <li><a href="/personal-injury/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Personal Injury</a></li>
            <li><a href="/employment-law/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Employment Law</a></li>
            <li><a href="/criminal-law/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Criminal Law</a></li>
          </ul>
        </div>
        <div>
          <h4 style="font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-bottom:12px">eSolicitors</h4>
          <ul style="list-style:none;display:flex;flex-direction:column;gap:8px">
            <li><a href="/about/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">About</a></li>
            <li><a href="/privacy/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Privacy</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:18px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px">
      <span style="font-size:.75rem;color:rgba(255,255,255,0.25)">2026 eSolicitors.ie</span>
      <span style="font-size:.72rem;color:rgba(255,255,255,0.2);max-width:480px">eSolicitors.ie is a referral service, not a law firm.</span>
    </div>
  </div>
</footer>
</body>
</html>"""

# Find all hub pages that have case cards
hub_files = sorted(set(
    glob.glob("./**/*.html", recursive=True) +
    glob.glob("./*.html")
))

generated = 0
linked = 0

for hub_path in hub_files:
    if '.github' in hub_path or '/api/' in hub_path:
        continue

    # Skip story pages (they're 3 levels deep like ./pi/dog-bite/aoife-dublin/)
    parts = hub_path.replace('./', '').split('/')
    if len(parts) > 3:
        continue

    try:
        with open(hub_path, 'r', encoding='utf-8') as f:
            hub_content = f.read()
    except:
        continue

    if 'case-card' not in hub_content:
        continue

    # Extract case cards: name, desc, result
    cards = re.findall(
        r'<div class="case-card"[^>]*>.*?<div class="case-name">([^<]+)</div>.*?<div class="case-desc">([^<]+)</div>.*?<div class="case-result">([^<]+)</div>',
        hub_content,
        flags=re.DOTALL
    )

    if not cards:
        continue

    # Derive hub folder from file path e.g. ./personal-injury/dog-bite/index.html -> personal-injury/dog-bite
    hub_folder = os.path.dirname(hub_path).lstrip('./')
    hub_url = '/' + hub_folder + '/' if hub_folder else '/'

    # Get page title for context
    title_match = re.search(r'<title>([^<]+)</title>', hub_content)
    page_title = title_match.group(1) if title_match else hub_folder

    print(f"\n{hub_path} — {len(cards)} cards")

    updated_hub = hub_content

    for name_loc, desc, result in cards:
        name_loc = name_loc.strip()
        desc = desc.strip()
        result = result.strip()

        # Generate slug from name + location
        story_slug = slugify(name_loc.replace(', ', '-').replace(',', '-'))
        story_folder = f"./{hub_folder}/{story_slug}"
        story_path = f"{story_folder}/index.html"
        story_url = f"/{hub_folder}/{story_slug}/"

        # Generate story page if it doesn't exist
        if not os.path.exists(story_path):
            print(f"  Generating: {story_url}")
            back_link = f'<div style="background:var(--navy-mid,#162d52);padding:8px 5%"><a href="{hub_url}" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:.82rem">← Back to {page_title.split("|")[0].strip()}</a></div>'

            prompt = (
                f"Write a story page for eSolicitors.ie.\n\n"
                f"Person: {name_loc}\n"
                f"Situation: {desc}\n"
                f"Outcome: {result}\n"
                f"Page context: {page_title}\n"
                f"Hub URL: {hub_url}\n\n"
                f"After the nav, insert this exact HTML on its own line:\n{back_link}\n\n"
                f"End the page body content after the time limit warning. Do not add footer or closing body/html tags — those will be added separately."
            )

            html = call_claude(SYSTEM, prompt)

            if html:
                html = re.sub(r'^```html\s*', '', html.strip())
                html = re.sub(r'\s*```$', '', html.strip())
                # Remove any </body></html> Claude might add
                html = re.sub(r'\s*</body>\s*</html>\s*$', '', html).rstrip()
                # Remove any sarah.js Claude might add
                html = re.sub(r'<script src="/sarah\.js"[^>]*></script>', '', html)

                os.makedirs(story_folder, exist_ok=True)
                with open(story_path, 'w', encoding='utf-8') as f:
                    f.write(html + "\n" + CTA_FOOTER)
                print(f"    Saved: {story_path}")
                generated += 1
                time.sleep(0.8)
            else:
                print(f"    FAILED: {story_path}")
                continue
        else:
            print(f"  Exists: {story_url}")

        # Link the card on the hub page
        old_card = (
            f'<div class="case-card">'
            f'<div class="case-name">{name_loc}</div>'
        )
        new_card = (
            f'<a href="{story_url}" class="case-card" style="text-decoration:none;display:block;cursor:pointer;">'
            f'<div class="case-name">{name_loc}</div>'
        )
        # Also handle cards that are already <a> tags
        if f'href="{story_url}"' not in updated_hub and old_card in updated_hub:
            updated_hub = updated_hub.replace(old_card, new_card, 1)
            # Close the card div -> close the <a> tag
            # Find position after this card's case-result div
            pos = updated_hub.find(new_card)
            result_end = updated_hub.find('</div>', updated_hub.find('case-result', pos)) + 6
            updated_hub = updated_hub[:result_end] + '</a>' + updated_hub[result_end:]
            linked += 1
            print(f"    Linked: {name_loc}")

    # Save updated hub page
    if updated_hub != hub_content:
        with open(hub_path, 'w', encoding='utf-8') as f:
            f.write(updated_hub)

print(f"\nDone. Generated: {generated} pages, Linked: {linked} cards.")
