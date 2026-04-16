import glob
import re

files = glob.glob("./*/*/*/index.html") + glob.glob("./*/*/*/*/index.html")
files = list(set(files))

fixed = 0

for filepath in sorted(files):
    if '.github' in filepath or '/api/' in filepath:
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    if 'Sound familiar' not in content:
        continue

    original = content

    # Remove sarah.js injected after footer
    content = re.sub(r'\s*<script src="/sarah\.js"[^>]*></script>\s*(?=</body>)', '', content)

    # Fill the empty Sarah container div (multiline)
    content = content.replace(
        '  <div style="max-width:480px;margin:0 auto">\n  </div>',
        '  <div style="max-width:480px;margin:0 auto">\n    <script src="/sarah.js" data-mode="inline"></script>\n  </div>'
    )

    # Fill empty div (single line)
    content = content.replace(
        '<div style="max-width:480px;margin:0 auto"></div>',
        '<div style="max-width:480px;margin:0 auto"><script src="/sarah.js" data-mode="inline"></script></div>'
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
        fixed += 1

print(f"\nDone. Fixed {fixed} story pages.")
