import glob
import re

files = sorted(set(
    glob.glob("./**/*.html", recursive=True) +
    glob.glob("./*.html")
))

fixed = 0

for filepath in files:
    if '.github' in filepath or '/api/' in filepath:
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    if 'stories-section' not in content:
        continue

    original = content

    # Fix 1: Remove the outer duplicate wrapper that contains the stories-section
    # Pattern: <section class="section"><div class="section-label">Real Situations</div><h2...><section class="stories-section"...
    content = re.sub(
        r'<section class="section">\s*<div class="section-label">Real Situations</div>\s*<h2[^>]*>What happened to people just like you</h2>\s*(?=<section class="stories-section")',
        '',
        content
    )

    # Fix 2: Close the unclosed outer section tag after stories-section ends
    # After </section> (stories-section close), there may be an orphan </section>
    content = re.sub(
        r'(</section>\s*)\n(\s*\n\s*<div class="page-wrap">|</div>\s*\n\s*<section)',
        r'\2',
        content
    )

    # Fix 3: Story card colors — make them dark navy background like homepage
    # Replace light cream card style with dark style
    content = content.replace(
        '.story-card{background:#fff;border:1px solid var(--border);border-radius:12px;padding:22px;text-decoration:none;transition:border-color .2s,box-shadow .2s;display:flex;flex-direction:column}',
        '.story-card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:22px;text-decoration:none;transition:background .2s,border-color .2s,transform .2s;display:flex;flex-direction:column}'
    )
    content = content.replace(
        '.story-card:hover{border-color:rgba(200,146,42,.4);box-shadow:0 8px 28px rgba(12,31,61,.08)}',
        '.story-card:hover{background:rgba(255,255,255,0.09);border-color:rgba(200,146,42,.35);transform:translateY(-2px)}'
    )
    content = content.replace(
        '.story-tag{display:inline-block;background:rgba(200,146,42,.1);color:var(--gold);padding:3px 9px;border-radius:4px;font-size:.68rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:12px}',
        '.story-tag{display:inline-block;background:rgba(200,146,42,.12);border:1px solid rgba(200,146,42,.25);color:var(--gold-light,#e8b04a);padding:3px 10px;border-radius:100px;font-size:.68rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;margin-bottom:12px;width:fit-content}'
    )
    content = content.replace(
        '.story-title{font-family:\'Playfair Display\',serif;font-size:.97rem;font-weight:700;color:var(--navy);line-height:1.35;margin-bottom:10px;flex:1}',
        '.story-title{font-family:\'Playfair Display\',serif;font-size:.97rem;font-weight:700;color:#fff;line-height:1.4;margin-bottom:10px;flex:1;font-style:italic}'
    )
    content = content.replace(
        '.story-person{color:var(--text-mid);font-weight:600}',
        '.story-person{color:rgba(255,255,255,0.6);font-weight:600}'
    )

    # Fix story-outcome and story-read colors
    if '.story-outcome' not in content or 'rgba(255,255,255' not in content.split('.story-outcome')[1][:50]:
        content = content.replace(
            '.story-outcome{',
            '.story-outcome{color:#4ade80;font-weight:700;font-size:.72rem;'
        )

    if '.story-read' in content:
        content = re.sub(
            r'\.story-read\{[^}]*\}',
            '.story-read{font-size:.75rem;color:var(--gold,#c8922a);font-weight:600}',
            content
        )

    # Fix 4: Make stories-section background navy
    content = content.replace(
        '<section class="stories-section" id="stories">\n  <div style="max-width:1200px;margin:0 auto;padding:0 5%">',
        '<section class="stories-section" id="stories" style="background:var(--navy,#0c1f3d);padding:60px 0">\n  <div style="max-width:1200px;margin:0 auto;padding:0 5%">'
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
        fixed += 1

print(f"\nDone. Fixed {fixed} files.")
