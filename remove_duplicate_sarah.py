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

    # Pages that have their own built-in chat (hero-form, chatInput, eSolicitors Assistant)
    has_own_chat = (
        'class="hero-form"' in content or
        'hero-form-wrap' in content or
        'chatInput' in content or
        'eSolicitors Assistant' in content or
        'sendMessage' in content
    )

    if not has_own_chat:
        continue

    if 'sarah.js' not in content:
        continue

    original = content

    # Remove the sarah.js injection
    content = re.sub(r'\s*<script src="/sarah\.js"[^>]*></script>', '', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Removed duplicate sarah.js: {filepath}")
        fixed += 1

print(f"\nDone. Fixed {fixed} files.")
