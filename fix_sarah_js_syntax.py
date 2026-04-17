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

    if 'source:window.location.pathname' not in content:
        continue

    original = content

    # Fix the broken fetch call - missing closing }) for fetch
    content = content.replace(
        'source:window.location.pathname});}}catch(e)',
        'source:window.location.pathname})});}}catch(e)'
    )
    # Also fix variant without space
    content = content.replace(
        "source:window.location.pathname});}}\ncatch(e)",
        "source:window.location.pathname})}); }}\ncatch(e)"
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
        fixed += 1

print(f"\nDone. Fixed {fixed} files.")
