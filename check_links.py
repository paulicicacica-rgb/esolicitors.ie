import glob
import re
import os

files = sorted(glob.glob("./**/*.html", recursive=True) + glob.glob("./*.html"))

broken = []
checked = 0

for filepath in files:
    if '.github' in filepath:
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    # Find all internal href links
    links = re.findall(r'href="(/[^"#?]*)"', content)

    for link in links:
        # Skip external-looking paths and anchors
        if link.startswith('//') or link == '/':
            continue

        # Convert URL to file path
        # /personal-injury/dog-bite/ -> ./personal-injury/dog-bite/index.html
        # /personal-injury/dog-bite -> ./personal-injury/dog-bite/index.html or .html
        path = link.rstrip('/')

        candidates = [
            '.' + path + '/index.html',
            '.' + path + '.html',
            '.' + path,
        ]

        exists = any(os.path.exists(c) for c in candidates)

        if not exists:
            broken.append({
                'source': filepath,
                'link': link
            })

        checked += 1

# Print results
print(f"\nChecked {checked} links across {len(files)} files")
print(f"Broken links found: {len(broken)}\n")

# Group by link target to avoid duplicates
seen = set()
unique_broken = []
for b in broken:
    if b['link'] not in seen:
        seen.add(b['link'])
        unique_broken.append(b)

print("UNIQUE BROKEN LINKS:")
print("=" * 60)
for b in sorted(unique_broken, key=lambda x: x['link']):
    print(f"  {b['link']}")
    print(f"    from: {b['source']}")

print(f"\nTotal unique broken targets: {len(unique_broken)}")
