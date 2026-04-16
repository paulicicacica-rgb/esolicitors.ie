import json
import glob
import re
import os

with open("stories_data.json", "r") as f:
    data = json.load(f)

CTA_AND_FOOTER = """
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
</body>
</html>"""

# Headings that signal garbage content — cut from here
CUT_TRIGGERS = [
    'Similar Cases',
    'Similar cases',
    'How ',  # "How Blessing Can Help" etc
    'Our Process',
    'Contact Information',
    'Contact Us',
    'Get Your Claim',
    'Get Legal Help',
    'Why Choose',
    'Why Us',
    'What We Do',
    'Our Services',
    'No Win No Fee',
    'Call Now',
]

story_files = []
for subcat in data["subcategories"]:
    for story in subcat["stories"]:
        path = f"./{data['practice_area']}/{subcat['slug']}/{story['slug']}/index.html"
        if os.path.exists(path):
            story_files.append((path, subcat, story))

print(f"Found {len(story_files)} story pages\n")

for filepath, subcat, story in story_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find earliest cut point based on trigger headings in <h2> or <h3>
    cut_pos = len(content)
    for trigger in CUT_TRIGGERS:
        # Match <h2> or <h3> containing the trigger text
        pattern = r'<(?:h2|h3|section)[^>]*>[^<]*' + re.escape(trigger)
        match = re.search(pattern, content, flags=re.IGNORECASE)
        if match and match.start() < cut_pos:
            # Walk back to opening of parent block
            before = content[:match.start()]
            candidates = [
                before.rfind('\n<section'),
                before.rfind('\n<div'),
                before.rfind('\n        <'),
                match.start()
            ]
            cut_pos = max([c for c in candidates if c >= 0] or [match.start()])

    # Slice content
    content = content[:cut_pos].rstrip()

    # Strip any leftover tags
    content = re.sub(r'\s*<script src="/sarah\.js"[^>]*></script>', '', content)
    content = re.sub(r'<footer[\s\S]*?</footer>', '', content, flags=re.DOTALL)
    content = re.sub(r'\s*</(?:main|body|html)>', '', content)

    # Close any obviously unclosed containers (rough but effective)
    open_divs = content.count('<div') - content.count('</div>')
    open_sections = content.count('<section') - content.count('</section')
    content = content.rstrip()
    for _ in range(min(open_sections, 5)):
        content += '\n</section>'
    for _ in range(min(open_divs, 10)):
        content += '\n</div>'

    # Add back button after </nav> if not present
    back_link = (
        f'\n<div style="background:var(--navy-mid,#162d52);padding:8px 5%">'
        f'<a href="{subcat["hub_url"]}" style="color:rgba(255,255,255,0.6);'
        f'text-decoration:none;font-size:.82rem;font-family:\'DM Sans\',sans-serif">'
        f'← Back to {subcat["label"]} claims</a></div>'
    )
    if 'Back to' not in content and '</nav>' in content:
        content = content.replace('</nav>', '</nav>' + back_link, 1)

    content = content + "\n" + CTA_AND_FOOTER

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Fixed: {filepath}")

print("\nDone.")
