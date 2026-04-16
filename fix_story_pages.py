import json
import glob
import re
import os
import time
import urllib.request
import urllib.error

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    raise Exception("ANTHROPIC_API_KEY not set")

with open("stories_data.json", "r") as f:
    data = json.load(f)

# Build slug -> subcat/story lookup
slug_lookup = {}
for subcat in data["subcategories"]:
    for story in subcat["stories"]:
        slug_lookup[story["slug"]] = {
            "name": story["name"],
            "location": story["location"],
            "subcat_slug": subcat["slug"],
            "subcat_label": subcat["label"],
            "hub_url": subcat["hub_url"],
        }

CTA_AND_FOOTER = """
<!-- CTA -->
<div style="background:var(--navy,#0c1f3d);padding:60px 5%;text-align:center">
  <div style="max-width:600px;margin:0 auto">
    <div style="font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold,#c8922a);margin-bottom:12px">Free Solicitor Matching</div>
    <h2 style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;color:#fff;margin-bottom:14px;line-height:1.2">Sound familiar?<br>You may have a case too.</h2>
    <p style="color:rgba(255,255,255,0.6);font-size:.95rem;margin-bottom:32px;line-height:1.7">Tell Sarah what happened. She will explain your options and match you with the right solicitor in your county — completely free, no obligation.</p>
  </div>
  <div style="max-width:480px;margin:0 auto">
    <script src="/sarah.js" data-mode="inline"></script>
  </div>
</div>

<!-- FOOTER -->
<footer style="background:#080f1e;padding:36px 5%;font-family:'DM Sans',sans-serif">
  <div style="max-width:1100px;margin:0 auto">
    <div style="display:flex;flex-wrap:wrap;gap:32px;justify-content:space-between;margin-bottom:28px">
      <div>
        <a href="/" style="font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:#fff;text-decoration:none">e<span style="color:var(--gold,#c8922a)">Solicitors</span>.ie</a>
        <p style="font-size:.8rem;color:rgba(255,255,255,0.35);margin-top:8px;max-width:240px;line-height:1.6">Ireland's free solicitor matching service. Qualified solicitors across all 26 counties.</p>
      </div>
      <div style="display:flex;gap:48px;flex-wrap:wrap">
        <div>
          <h4 style="font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-bottom:12px">Navigate</h4>
          <ul style="list-style:none;display:flex;flex-direction:column;gap:8px">
            <li><a href="/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Home</a></li>
            <li><a href="/personal-injury/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Personal Injury</a></li>
            <li><a href="/criminal-law/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Criminal Law</a></li>
            <li><a href="/employment-law/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Employment Law</a></li>
          </ul>
        </div>
        <div>
          <h4 style="font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,0.5);margin-bottom:12px">eSolicitors</h4>
          <ul style="list-style:none;display:flex;flex-direction:column;gap:8px">
            <li><a href="/about/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">About</a></li>
            <li><a href="/privacy/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Privacy</a></li>
            <li><a href="/for-solicitors/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">For Solicitors</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:18px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px">
      <span style="font-size:.75rem;color:rgba(255,255,255,0.25)">2026 eSolicitors.ie</span>
      <span style="font-size:.72rem;color:rgba(255,255,255,0.2);max-width:480px">eSolicitors.ie is a referral service, not a law firm. Always consult a qualified solicitor for your specific situation.</span>
    </div>
  </div>
</footer>
"""

def call_claude(prompt):
    payload = json.dumps({
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 2000,
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
        print(f"    API error {e.code}: {e.read().decode()}")
        return None

# Find all generated story pages
story_files = []
for subcat in data["subcategories"]:
    for story in subcat["stories"]:
        path = f"./{data['practice_area']}/{subcat['slug']}/{story['slug']}/index.html"
        if os.path.exists(path):
            story_files.append((path, subcat, story))

print(f"Found {len(story_files)} story pages to fix\n")

for filepath, subcat, story in story_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changed = False

    # 1. Remove Similar Cases section
    content = re.sub(
        r'<section[^>]*>\s*<h2[^>]*>\s*Similar Cases\s*</h2>.*?</section>',
        '',
        content,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 2. Remove any existing sarah.js injection
    content = re.sub(r'\s*<script src="/sarah\.js"[^>]*></script>', '', content)

    # 3. Check if page is truncated (no </body> or no </html>)
    is_truncated = '</body>' not in content or '</html>' not in content

    if is_truncated:
        print(f"  Truncated — completing: {filepath}")
        # Get the last 800 chars as context
        tail = content[-800:]
        completion = call_claude(
            f"This HTML page was cut off mid-content. Continue and complete it naturally. "
            f"Do NOT restart or repeat content. Just continue from exactly where it stopped. "
            f"End with a closing </section> and </main> or </div> as needed to close open tags. "
            f"Do NOT include <html>, <head>, <body>, footer or any sarah.js script tag — just the missing middle HTML.\n\n"
            f"The page is about: {story['name']} from {story['location']} — {subcat['label']} claim in Ireland.\n\n"
            f"Page ends with:\n{tail}"
        )
        if completion:
            # Remove </body></html> if present in truncated content before appending
            content = re.sub(r'\s*</body>\s*</html>\s*$', '', content).rstrip()
            content += "\n" + completion.strip()
            changed = True
            time.sleep(0.5)

    # 4. Remove existing footer and closing tags so we can add our own
    content = re.sub(r'<footer[\s\S]*?</footer>', '', content, flags=re.DOTALL)
    content = re.sub(r'\s*</body>\s*</html>\s*$', '', content).rstrip()

    # 5. Add back button near top (after breadcrumb if exists, else after nav)
    back_link = f'<div style="background:var(--navy-mid,#162d52);padding:8px 5%"><a href="{subcat["hub_url"]}" style="color:rgba(255,255,255,0.6);text-decoration:none;font-size:.82rem;font-family:\'DM Sans\',sans-serif">← Back to {subcat["label"]} claims</a></div>'

    if 'class="breadcrumb"' in content and back_link not in content:
        content = re.sub(
            r'(</div>\s*)(<!-- HERO|<section|<div class="hero)',
            back_link + r'\n\1\2',
            content,
            count=1
        )
    elif back_link not in content:
        content = content.replace('</nav>', '</nav>\n' + back_link, 1)

    # 6. Inject CTA + footer before </html> or at end
    content = content.rstrip() + "\n" + CTA_AND_FOOTER + "\n</body>\n</html>"
    changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Fixed: {filepath}")

print("\nDone.")
