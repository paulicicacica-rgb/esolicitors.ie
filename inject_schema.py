#!/usr/bin/env python3
"""
Schema injection script for eSolicitors.ie
Injects JSON-LD structured data into all HTML files in the public/ directory.

Schema types injected:
- Organization (homepage only)
- LegalService (all pages)
- BreadcrumbList (all pages)
- FAQPage (pages with FAQ sections)
"""

import os
import re
import json
from pathlib import Path

BASE_URL = "https://www.esolicitors.ie"
PUBLIC_DIR = Path("public")

ORGANIZATION_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "eSolicitors.ie",
    "url": BASE_URL,
    "logo": f"{BASE_URL}/images/logo-dark.svg",
    "description": "Ireland's free AI-powered legal platform connecting people to qualified solicitors across all 32 counties.",
    "areaServed": {
        "@type": "Country",
        "name": "Ireland"
    },
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer support",
        "availableLanguage": ["English", "Irish", "Romanian", "Polish", "Portuguese", "Arabic", "Spanish", "Russian"]
    },
    "sameAs": [
        "https://esolicitors.ie"
    ]
}

LEGAL_SERVICE_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "LegalService",
    "name": "eSolicitors.ie",
    "url": BASE_URL,
    "description": "Free AI-powered legal guidance and solicitor matching service covering all of Ireland.",
    "provider": {
        "@type": "Organization",
        "name": "eSolicitors.ie"
    },
    "areaServed": {
        "@type": "Country",
        "name": "Ireland"
    },
    "serviceType": "Legal referral and guidance",
    "availableLanguage": ["English", "Romanian", "Polish", "Portuguese", "Arabic", "Spanish", "Russian"]
}


def get_page_title(soup_text):
    """Extract title from HTML."""
    match = re.search(r'<title[^>]*>(.*?)</title>', soup_text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return "eSolicitors.ie"


def get_h1(soup_text):
    """Extract first H1 from HTML."""
    match = re.search(r'<h1[^>]*>(.*?)</h1>', soup_text, re.IGNORECASE | re.DOTALL)
    if match:
        # Strip inner tags
        text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
        return text
    return None


def get_faq_items(html):
    """
    Extract FAQ Q&A pairs from common patterns:
    - <details><summary>Q</summary>A</details>
    - elements with class containing 'faq', 'accordion', 'question'
    - <dt>Q</dt><dd>A</dd> patterns
    Returns list of {question, answer} dicts, max 10.
    """
    faqs = []

    # Pattern 1: <details><summary>Q</summary>A</details>
    details_pattern = re.finditer(
        r'<details[^>]*>.*?<summary[^>]*>(.*?)</summary>(.*?)</details>',
        html, re.IGNORECASE | re.DOTALL
    )
    for m in details_pattern:
        q = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        a = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if q and a and len(q) > 10:
            faqs.append({"question": q, "answer": a[:500]})

    # Pattern 2: dt/dd pairs
    if not faqs:
        dl_pattern = re.finditer(
            r'<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>',
            html, re.IGNORECASE | re.DOTALL
        )
        for m in dl_pattern:
            q = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            a = re.sub(r'<[^>]+>', '', m.group(2)).strip()
            if q and a and len(q) > 10:
                faqs.append({"question": q, "answer": a[:500]})

    # Pattern 3: faq-question / faq-answer class pairs
    if not faqs:
        faq_q_pattern = re.findall(
            r'class="[^"]*(?:faq-question|question)[^"]*"[^>]*>(.*?)<',
            html, re.IGNORECASE | re.DOTALL
        )
        faq_a_pattern = re.findall(
            r'class="[^"]*(?:faq-answer|answer)[^"]*"[^>]*>(.*?)</(?:p|div)',
            html, re.IGNORECASE | re.DOTALL
        )
        for q, a in zip(faq_q_pattern, faq_a_pattern):
            q = re.sub(r'<[^>]+>', '', q).strip()
            a = re.sub(r'<[^>]+>', '', a).strip()
            if q and a:
                faqs.append({"question": q, "answer": a[:500]})

    return faqs[:10]


def build_breadcrumb(file_path):
    """Build BreadcrumbList schema from file path."""
    parts = file_path.parts  # e.g. ('public', 'criminal-law', 'drink-driving', 'index.html')
    
    items = [{
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": BASE_URL
    }]

    url_parts = [p for p in parts[1:] if p != "index.html"]  # strip 'public' and 'index.html'
    
    cumulative = BASE_URL
    for i, part in enumerate(url_parts):
        cumulative += f"/{part}"
        # Make a readable name from slug
        name = part.replace("-", " ").replace("_", " ").title()
        items.append({
            "@type": "ListItem",
            "position": i + 2,
            "name": name,
            "item": cumulative
        })

    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }


def build_faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in faqs
        ]
    }


def already_has_schema(html):
    """Check if page already has JSON-LD schema."""
    return 'application/ld+json' in html


def build_script_tag(schema_obj):
    return f'<script type="application/ld+json">\n{json.dumps(schema_obj, indent=2, ensure_ascii=False)}\n</script>'


def inject_schemas(html, schemas):
    """Inject all schema script tags before </head>."""
    combined = "\n".join(build_script_tag(s) for s in schemas)
    # Insert before </head>
    return re.sub(r'(</head>)', f'{combined}\n\\1', html, count=1, flags=re.IGNORECASE)


def process_file(file_path):
    """Process a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
    except Exception as e:
        print(f"  ERROR reading {file_path}: {e}")
        return False

    if already_has_schema(html):
        return False  # Skip — already injected

    if '</head>' not in html.lower():
        return False  # Malformed — skip

    schemas = []

    # Determine relative path from public/
    rel_path = file_path.relative_to(PUBLIC_DIR)
    parts = rel_path.parts
    is_homepage = (rel_path == Path("index.html") or parts == ("index.html",))

    # 1. Organization — homepage only
    if is_homepage:
        schemas.append(ORGANIZATION_SCHEMA)

    # 2. LegalService — all pages
    schemas.append(LEGAL_SERVICE_SCHEMA)

    # 3. BreadcrumbList — all pages with depth > 0
    if not is_homepage:
        schemas.append(build_breadcrumb(file_path))

    # 4. FAQPage — only if we find FAQ content
    faqs = get_faq_items(html)
    if faqs:
        schemas.append(build_faq_schema(faqs))

    new_html = inject_schemas(html, schemas)

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        return True
    except Exception as e:
        print(f"  ERROR writing {file_path}: {e}")
        return False


def main():
    if not PUBLIC_DIR.exists():
        print(f"ERROR: '{PUBLIC_DIR}' directory not found. Run from repo root.")
        return

    html_files = list(PUBLIC_DIR.rglob("*.html"))
    total = len(html_files)
    print(f"Found {total} HTML files in {PUBLIC_DIR}/")

    injected = 0
    skipped = 0
    errors = 0

    for i, file_path in enumerate(html_files, 1):
        result = process_file(file_path)
        if result is True:
            injected += 1
            if injected <= 10 or injected % 50 == 0:
                print(f"  [+] {file_path}")
        elif result is False:
            skipped += 1

        if i % 100 == 0:
            print(f"Progress: {i}/{total} processed...")

    print(f"\n{'='*50}")
    print(f"Schema injection complete:")
    print(f"  Injected : {injected} files")
    print(f"  Skipped  : {skipped} files (already had schema or malformed)")
    print(f"  Total    : {total} files")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
