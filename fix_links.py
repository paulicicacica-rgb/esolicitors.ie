import glob 
import re
import os
import shutil

# These are folders created from stories_data.json with wrong names
# They don't match any hub page and cause 404s
ORPHAN_PATTERNS = [
    "./personal-injury/cycling-pedestrian-accident",
    "./personal-injury/road-traffic-accident",
    "./personal-injury/slip-and-fall",
    "./personal-injury/workplace-injury",
    "./personal-injury/property-accident",
    "./personal-injury/holiday-travel-accident",
    "./personal-injury/dog-bite/aoife-dublin",
    "./personal-injury/dog-bite/tomas-galway",
    "./personal-injury/dog-bite/blessing-limerick",
    "./personal-injury/dog-bite/piotr-kildare",
]

print("Removing orphaned folders...")
for pattern in ORPHAN_PATTERNS:
    if os.path.exists(pattern):
        shutil.rmtree(pattern)
        print(f"  Removed: {pattern}")
    else:
        print(f"  Not found: {pattern}")

# Now find all hub pages with unlinked cards and check if story exists
files = sorted(set(
    glob.glob("./**/*.html", recursive=True) +
    glob.glob("./*.html")
))

print("\nChecking card links...")
fixed = 0

for filepath in files:
    if '.github' in filepath or '/api/' in filepath:
        continue
    
    # Skip story pages (3+ levels deep)
    parts = filepath.replace('./', '').split('/')
    if len(parts) > 3:
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    if 'case-card' not in content:
        continue

    hub_folder = os.path.dirname(filepath).lstrip('./')
    original = content

    # Find all unlinked cards
    cards = re.findall(
        r'<div class="case-card">\s*<div class="case-name">([^<]+)</div>',
        content
    )

    for name_loc in cards:
        name_loc = name_loc.strip()
        # Generate slug
        import unicodedata
        slug = unicodedata.normalize('NFD', name_loc)
        slug = ''.join(c for c in slug if unicodedata.category(c) != 'Mn')
        slug = slug.lower().strip()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s,]+', '-', slug).strip('-')

        story_path = f"./{hub_folder}/{slug}/index.html"
        story_url = f"/{hub_folder}/{slug}/"

        if not os.path.exists(story_path):
            print(f"  Missing page: {story_path}")
            continue

        # Link the card
        old_card = f'<div class="case-card">\n<div class="case-name">{name_loc}</div>'
        old_card2 = f'<div class="case-card"><div class="case-name">{name_loc}</div>'
        new_card = f'<a href="{story_url}" class="case-card" style="text-decoration:none;display:block;cursor:pointer;"><div class="case-name">{name_loc}</div>'

        if old_card in content:
            content = content.replace(old_card, new_card, 1)
            # Close the a tag after case-result
            pos = content.find(new_card)
            result_end = content.find('</div>', content.find('case-result', pos)) + 6
            content = content[:result_end] + '</a>' + content[result_end:]
            print(f"  Linked: {name_loc} -> {story_url}")
            fixed += 1
        elif old_card2 in content:
            content = content.replace(old_card2, new_card, 1)
            pos = content.find(new_card)
            result_end = content.find('</div>', content.find('case-result', pos)) + 6
            content = content[:result_end] + '</a>' + content[result_end:]
            print(f"  Linked: {name_loc} -> {story_url}")
            fixed += 1

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print(f"\nDone. Fixed {fixed} card links.")
