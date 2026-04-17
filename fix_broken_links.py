import glob
import os

all_html = glob.glob("./**/*.html", recursive=True) + glob.glob("./*.html")

# Build index of all existing pages
existing_urls = set()
for f in all_html:
    url = f.lstrip('.')
    url = url.replace('/index.html', '/')
    url = url.replace('.html', '/')
    if not url.endswith('/'):
        url += '/'
    existing_urls.add(url)

print(f"Found {len(existing_urls)} existing pages")

# All fixes — broken → destination
# If destination doesn't exist, falls back to nearest parent that does
FIXES = {
    '/conveyancing':              '/property-law/',
    '/conveyancing/':             '/property-law/',
    '/employment':                '/employment-law/',
    '/employment/':               '/employment-law/',
    '/family':                    '/family-law/',
    '/property':                  '/property-law/',
    '/practice-areas':            '/',
    '/services':                  '/',
    '/guide/':                    '/about/',
    '/how-it-works/':             '/#how',
    '/find-a-solicitor/':         '/chat.html',
    '/find-solicitor':            '/chat.html',
    '/find-solicitor/':           '/chat.html',
    '/for-solicitors/':           '/about/',
    '/debt-insolvency/':          '/debt-law/',
    '/workplace-injury/':         '/personal-injury/workplace-injury/',
    '/employment-law/equal-pay/': '/employment-law/discrimination/',
    '/criminal-law/drink-driving/':                      '/criminal-law/driving-offences/',
    '/criminal-law/drink-driving-ireland/':              '/criminal-law/driving-offences/',
    '/criminal-law/drug-driving-ireland/':               '/criminal-law/driving-offences/',
    '/criminal-law/no-insurance-ireland/':               '/criminal-law/driving-offences/',
    '/criminal-law/no-licence-ireland/':                 '/criminal-law/driving-offences/',
    '/criminal-law/dangerous-driving-ireland/':          '/criminal-law/driving-offences/',
    '/criminal-law/careless-driving-ireland/':           '/criminal-law/driving-offences/',
    '/criminal-law/hit-and-run-ireland/':                '/criminal-law/driving-offences/',
    '/criminal-law/driving-while-disqualified-ireland/': '/criminal-law/driving-offences/',
    '/personal-injury/holiday-travel-accident/rachel-dublin/': '/personal-injury/',
    '/personal-injury/property-accident/tomasz-kildare/':      '/personal-injury/',
    '/personal-injury/road-traffic-accident/kevin-limerick/':  '/personal-injury/road-traffic-accident/',
    '/personal-injury/slip-and-fall/marek-cork/':              '/personal-injury/slip-fall/marek-cork/',
    '/personal-injury/slip-and-fall/siobhan-dublin/':          '/personal-injury/slip-fall/',
    '/personal-injury/dog-bite/damien-cork/':                  '/personal-injury/dog-bite/',
    '/pl/nielegalny-wzrost-czynszu/':  '/pl/',
    '/pt-br/aumento-ilegal-aluguel/':  '/pt-br/',
    '/ro/crestere-ilegala-chirie/':    '/ro/',
    '/ro/viza-refuzata/':              '/ro/imigratie-irp/',
    '/ar/fasl-tashghili-ghayr-adil/':       '/ar/',
    '/ar/ghabn-min-sahib-amal-or-mansil/':  '/ar/',
    '/ar/hadith-tawsil/':                   '/ar/',
    '/ar/hijra-iqama/':                     '/ar/',
    '/ar/mashakel-ijar/':                   '/ar/',
    '/ar/nasl-wa-lujoo/':                   '/ar/',
    '/ar/qiyadat-sukr/':                    '/ar/',
    '/ar/talaq-firaq/':                     '/ar/',
    '/ar/tasrih-amal/':                     '/ar/',
}

# Verify each destination exists, fall back to parent if not
verified = {}
for broken, target in FIXES.items():
    if target in ('/#how', '/chat.html', '/'):
        verified[broken] = target
        continue
    check = target.rstrip('/') + '/'
    if check in existing_urls:
        verified[broken] = target
    else:
        # Walk up to find existing parent
        parts = [p for p in target.rstrip('/').split('/') if p]
        found = '/'
        while parts:
            parts.pop()
            parent = '/' + '/'.join(parts) + '/' if parts else '/'
            if parent in existing_urls:
                found = parent
                break
        verified[broken] = found
        if found != target:
            print(f"  Fallback: {broken} → {found} (wanted {target})")

# Apply to all files
fixed_files = 0
fixed_links = 0

for filepath in sorted(all_html):
    if '.github' in filepath:
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    original = content
    page_count = 0
    for broken, fixed in verified.items():
        old = f'href="{broken}"'
        new = f'href="{fixed}"'
        n = content.count(old)
        if n:
            content = content.replace(old, new)
            page_count += n
            fixed_links += n

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_files += 1
        print(f"Fixed {page_count} link(s): {filepath}")

print(f"\nDone. Fixed {fixed_links} links across {fixed_files} files.")
