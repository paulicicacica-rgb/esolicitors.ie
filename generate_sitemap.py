import glob
import os
from datetime import date

BASE_URL = "https://esolicitors.ie"
today = date.today().isoformat()

# Find all HTML files
files = sorted(set(
    glob.glob("./**/*.html", recursive=True) +
    glob.glob("./*.html")
))

# Priority rules
def get_priority(path):
    parts = path.replace('./', '').split('/')
    depth = len(parts)
    if depth == 1:  # root pages
        return "1.0"
    if depth == 2:  # hub pages like /personal-injury/index.html
        return "0.8"
    if depth == 3:  # subpages like /personal-injury/dog-bite/index.html
        return "0.7"
    return "0.6"  # story pages and deeper

def get_changefreq(path):
    parts = path.replace('./', '').split('/')
    depth = len(parts)
    if depth == 1:
        return "weekly"
    if depth == 2:
        return "weekly"
    return "monthly"

urls = []

for filepath in files:
    # Skip non-public files
    if any(x in filepath for x in ['.github', '/api/', 'node_modules']):
        continue

    # Convert filepath to URL
    path = filepath.replace('./', '').replace('\\', '/')

    # Remove index.html
    if path.endswith('/index.html'):
        url_path = '/' + path[:-len('index.html')]
    elif path == 'index.html':
        url_path = '/'
    elif path.endswith('.html'):
        url_path = '/' + path[:-5]
    else:
        continue

    # Clean trailing slash
    if url_path != '/' and url_path.endswith('/'):
        url_path = url_path.rstrip('/')

    full_url = BASE_URL + url_path

    urls.append({
        'url': full_url,
        'priority': get_priority(filepath),
        'changefreq': get_changefreq(filepath),
    })

# Build XML
lines = ['<?xml version="1.0" encoding="UTF-8"?>']
lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

for entry in urls:
    lines.append('  <url>')
    lines.append(f'    <loc>{entry["url"]}</loc>')
    lines.append(f'    <lastmod>{today}</lastmod>')
    lines.append(f'    <changefreq>{entry["changefreq"]}</changefreq>')
    lines.append(f'    <priority>{entry["priority"]}</priority>')
    lines.append('  </url>')

lines.append('</urlset>')

sitemap = '\n'.join(lines)

with open('./sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f"Generated sitemap.xml with {len(urls)} URLs")
