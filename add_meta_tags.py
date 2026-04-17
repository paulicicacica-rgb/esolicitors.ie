import glob
import re
import os

OG_IMAGE = "https://esolicitors.ie/og-image.jpg"
SITE_NAME = "eSolicitors.ie"
SITE_URL = "https://esolicitors.ie"

FAVICON_TAGS = '''<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="alternate icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">'''

files = sorted(glob.glob("./**/*.html", recursive=True) + glob.glob("./*.html"))

fixed = 0
skipped = 0

for filepath in files:
    if '.github' in filepath:
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    original = content

    # ── 1. Add favicon if missing ──
    if 'rel="icon"' not in content and '<head>' in content:
        content = content.replace('<head>', '<head>\n' + FAVICON_TAGS, 1)

    # ── 2. Get existing title and meta description ──
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else SITE_NAME

    desc_match = re.search(r'<meta name="description" content="([^"]*)"', content)
    desc = desc_match.group(1).strip() if desc_match else ""

    # If no description, build one from title
    if not desc:
        clean_title = title.replace(' | eSolicitors.ie', '').replace(' | esolicitors.ie', '').strip()
        desc = f"{clean_title} — Free solicitor matching in Ireland. Tell us what happened and we'll connect you with the right solicitor in your county. No cost, no obligation."
        # Add meta description
        if title_match:
            content = content.replace(
                f'<title>{title_match.group(1)}</title>',
                f'<title>{title_match.group(1)}</title>\n<meta name="description" content="{desc}">'
            )

    # ── 3. Build canonical URL from file path ──
    url_path = filepath.lstrip('.').replace('/index.html', '/').replace('.html', '/')
    if not url_path.startswith('/'):
        url_path = '/' + url_path
    canonical = SITE_URL + url_path

    # ── 4. Add OG tags if missing ──
    if 'og:title' not in content:
        og_tags = f'''<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title.replace(' | eSolicitors.ie', '')}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{canonical}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title.replace(' | eSolicitors.ie', '')}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMAGE}">
<link rel="canonical" href="{canonical}">'''

        # Insert before </head>
        content = content.replace('</head>', og_tags + '\n</head>', 1)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1
    else:
        skipped += 1

print(f"Done. Updated {fixed} files, skipped {skipped}.")
