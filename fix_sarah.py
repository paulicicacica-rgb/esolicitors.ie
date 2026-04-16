import glob, re

files = list(set(glob.glob("./**/*.html", recursive=True) + glob.glob("./*.html")))

SARAH_HERO = (
    '<div class="hero-form" style="padding:0;overflow:hidden;'
    'background:transparent;box-shadow:0 32px 64px rgba(0,0,0,0.3);border-radius:14px;">\n'
    '  <script src="/sarah.js" data-mode="inline-hero"></script>\n'
    '</div>'
)

SARAH_HERO_WRAP = (
    '<div class="hero-form-wrap" style="padding:0;overflow:hidden;'
    'background:transparent;box-shadow:0 40px 80px rgba(0,0,0,0.35);border-radius:16px;">\n'
    '  <script src="/sarah.js" data-mode="inline-hero"></script>\n'
    '</div>'
)

SARAH_BLOCK = (
    '<div style="background:var(--cream-dark);padding:0 5%">\n'
    '  <div style="max-width:540px;margin:0 auto;padding:40px 0">\n'
    '    <script src="/sarah.js" data-mode="inline"></script>\n'
    '  </div>\n'
    '</div>'
)

SARAH_CSS = "  #es-inline-wrap{margin:0!important;height:480px!important;border-radius:14px!important}\n"

for filepath in sorted(files):
    if '/api/' in filepath or '.github' in filepath:
        continue
    if filepath in ['./index.html', './chat.html']:
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    original = content

    # Remove any existing sarah.js tags first (clean slate)
    content = re.sub(r'\s*<script src="/sarah\.js"[^>]*></script>', '', content)

    # Replace hero-form-wrap (homepage style)
    if 'hero-form-wrap' in content:
        content = re.sub(
            r'<div class="hero-form-wrap"[^>]*>.*?</div>',
            SARAH_HERO_WRAP,
            content,
            flags=re.DOTALL
        )
        if 'es-inline-wrap' not in content:
            content = content.replace('</style>', SARAH_CSS + '</style>', 1)
        print(f"  hero-form-wrap replaced: {filepath}")

    # Replace hero-form (section pages like criminal-law, employment etc)
    elif 'class="hero-form"' in content:
        content = re.sub(
            r'<div class="hero-form"[^>]*>.*?</div>(?=\s*</div>\s*</section>)',
            SARAH_HERO,
            content,
            flags=re.DOTALL
        )
        if 'es-inline-wrap' not in content:
            content = content.replace('</style>', SARAH_CSS + '</style>', 1)
        print(f"  hero-form replaced: {filepath}")

    # Replace scan-box wrapper (inner pages)
    if re.search(r'<div[^>]*cream-dark[^>]*>\s*<div[^>]*>\s*<div class="scan-box">', content, re.DOTALL):
        content = re.sub(
            r'<div[^>]*cream-dark[^>]*>\s*<div[^>]*>\s*<div class="scan-box">.*?</div>\s*</div>\s*</div>',
            SARAH_BLOCK,
            content,
            flags=re.DOTALL
        )
        print(f"  scan-box replaced: {filepath}")

    # Only inject at bottom if Sarah isn't already embedded in the page
    has_hero = 'hero-form-wrap' in original or 'class="hero-form"' in original
    has_scanbox = 'class="scan-box"' in original
    has_own_chat = 'chat-wrap' in original or 'chatInput' in original
    if not has_hero and not has_scanbox and not has_own_chat:
        content = content.replace('</body>', '  <script src="/sarah.js" data-mode="inline"></script>\n</body>')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Saved: {filepath}")
    else:
        print(f"  No change: {filepath}")

print("\nDone.")
