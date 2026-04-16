import json
import glob
import re

with open("stories_data.json", "r") as f:
    data = json.load(f)

# Build lookup: "Firstname, Location" -> url
# e.g. "Aoife, Dublin" -> "/personal-injury/dog-bite/aoife-dublin/"
lookup = {}
for subcat in data["subcategories"]:
    for story in subcat["stories"]:
        key = f"{story['name']}, {story['location']}"
        url = f"/{data['practice_area']}/{subcat['slug']}/{story['slug']}/"
        lookup[key] = url
        # Also try without accent (Tomás -> Tomas)
        key_plain = key.replace("á","a").replace("é","e").replace("ó","o").replace("í","i").replace("ú","u")
        lookup[key_plain] = url

print("Slug lookup built:", len(lookup), "entries")

files = list(set(glob.glob("./**/*.html", recursive=True) + glob.glob("./*.html")))

total = 0

for filepath in sorted(files):
    if ".github" in filepath or "/api/" in filepath:
        continue
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        continue

    if "case-card" not in content:
        continue

    original = content

    def replace_card(m):
        name_loc = m.group(1)  # e.g. "Aoife, Dublin"
        desc = m.group(2)
        result = m.group(3)
        url = lookup.get(name_loc)
        if not url:
            # try stripping accents
            plain = name_loc.replace("á","a").replace("é","e").replace("ó","o").replace("í","i").replace("ú","u")
            url = lookup.get(plain)
        if url:
            return (
                f'<a href="{url}" class="case-card" style="text-decoration:none;display:block;cursor:pointer;">'
                f'<div class="case-name">{name_loc}</div>'
                f'<div class="case-desc">{desc}</div>'
                f'<div class="case-result">{result}</div>'
                f'</a>'
            )
        else:
            print(f"  No slug for: {name_loc}")
            return m.group(0)

    content = re.sub(
        r'<div class="case-card">\s*<div class="case-name">([^<]+)</div>\s*<div class="case-desc">([^<]+)</div>\s*<div class="case-result">([^<]+)</div>\s*',
        replace_card,
        content
    )

    # Add hover style for case-card links if not present
    if "case-card:hover" not in content:
        content = content.replace(
            ".case-name {",
            ".case-card:hover { border-color: var(--gold); transform: translateY(-2px); box-shadow: 0 6px 20px rgba(12,31,61,0.1); }\n  .case-name {"
        )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Updated: {filepath}")
        total += 1

print(f"\nDone. {total} file(s) updated.")
