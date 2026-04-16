import glob, re

files = list(set(glob.glob("./**/*.html", recursive=True) + glob.glob("./*.html")))

SARAH_BLOCK = (
    '<div style="background:var(--cream-dark);padding:0 5%">\n'
    '  <div style="max-width:540px;margin:0 auto;padding:40px 0">\n'
    '    <script src="/sarah.js" data-mode="inline"></script>\n'
    '  </div>\n'
    '</div>'
)

SARAH_HERO = (
    '<div class="hero-form-wrap" style="padding:0;overflow:hidden;'
    'background:transparent;box-shadow:0 40px 80px rgba(0,0,0,0.35);border-radius:16px;">\n'
    '  <script src="/sarah.js" data-mode="inline-hero"></script>\n'
    '</div>'
)

SARAH_CSS = "  #es-inline-wrap{margin:0!important;height:480px!important;border-radius:16px!important}\n"

for filepath in sorted(files):
    if '/api/' in filepath or '.github' in filepath:
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    original = content

    # Replace scan-box wrapper
    content = re.sub(
        r'<div[^>]*cream-dark[^>]*>\s*<div[^>]*>\s*<div class="scan-box">.*?</div>\s*</div>\s*</div>',
        SARAH_BLOCK,
        content,
        flags=re.DOTALL
    )

    # Replace hero form wrap
    if 'hero-form-wrap' in content:
        content = re.sub(
            r'<div class="hero-form-wrap"[^>]*>.*?</div>',
            SARAH_HERO,
            content,
            flags=re.DOTALL
        )
        if 'es-inline-wrap' not in content:
            content = content.replace('</style>', SARAH_CSS + '</style>', 1)

    # Remove any existing sarah.js tags then re-inject once
    content = re.sub(r'\s*<script src="/sarah\.js"[^>]*></script>', '', content)
    content = content.replace('</body>', '  <script src="/sarah.js" data-mode="inline"></script>\n</body>')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
    else:
        print(f"No change: {filepath}")

print("Done.")
