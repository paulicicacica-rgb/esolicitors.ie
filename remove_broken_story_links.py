import glob
import re
import os

# Replace any <a href="/stories/..."> cards with real story page links
# These are the old hardcoded cards linking to non-existent /stories/ URLs

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

    if '/stories/' not in content:
        continue

    original = content

    # Remove entire story-card <a> blocks that link to /stories/
    content = re.sub(
        r'<a href="/stories/[^"]*"[^>]*class="story-card"[^>]*>.*?</a>',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<a class="story-card"[^>]*href="/stories/[^"]*"[^>]*>.*?</a>',
        '',
        content,
        flags=re.DOTALL
    )

    # Also fix footer links to /stories/
    content = re.sub(
        r'<li><a href="/stories/[^"]*">[^<]*</a></li>\s*',
        '',
        content
    )
    content = re.sub(
        r'<a href="/stories/">[^<]*</a>',
        '<a href="/personal-injury/">Real Stories</a>',
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
        fixed += 1

print(f"\nDone. Fixed {fixed} files.")
