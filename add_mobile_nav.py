import glob
import re

files = list(set(glob.glob("./**/*.html", recursive=True) + glob.glob("./*.html")))

# The hamburger button HTML — inserted inside nav before closing tag
HAMBURGER_BTN = '<button class="nav-hamburger" onclick="this.closest(\'nav\').classList.toggle(\'nav-open\')" aria-label="Menu"><span></span><span></span><span></span></button>'

# CSS to inject before </style>
MOBILE_NAV_CSS = """
  /* ── MOBILE NAV ── */
  .nav-hamburger {
    display: none;
    flex-direction: column;
    gap: 5px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 6px;
    z-index: 201;
  }
  .nav-hamburger span {
    display: block;
    width: 24px;
    height: 2px;
    background: rgba(255,255,255,0.8);
    border-radius: 2px;
    transition: all 0.3s ease;
  }
  .nav-open .nav-hamburger span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
  .nav-open .nav-hamburger span:nth-child(2) { opacity: 0; }
  .nav-open .nav-hamburger span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
  @media (max-width: 900px) {
    .nav-hamburger { display: flex; }
    .nav-links {
      display: none !important;
      position: fixed;
      top: 62px; left: 0; right: 0;
      background: var(--navy, #0c1f3d);
      flex-direction: column;
      padding: 20px 5% 28px;
      gap: 0 !important;
      border-bottom: 1px solid rgba(200,146,42,0.2);
      box-shadow: 0 8px 24px rgba(0,0,0,0.3);
      z-index: 199;
    }
    .nav-open .nav-links {
      display: flex !important;
    }
    .nav-links li { border-bottom: 1px solid rgba(255,255,255,0.07); }
    .nav-links a {
      display: block;
      padding: 14px 0;
      font-size: .95rem !important;
      color: rgba(255,255,255,0.8) !important;
    }
    .nav-links .nav-cta {
      margin-top: 12px;
      background: var(--gold, #c8922a) !important;
      color: var(--navy, #0c1f3d) !important;
      padding: 12px 20px !important;
      border-radius: 8px;
      text-align: center;
      display: block;
    }
  }
"""

total = 0

for filepath in sorted(files):
    if '.github' in filepath or '/api/' in filepath:
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    if 'nav-hamburger' in content:
        continue

    if '</nav>' not in content or 'nav-links' not in content:
        continue

    original = content

    # 1. Inject hamburger button before </nav>
    content = content.replace('</nav>', HAMBURGER_BTN + '\n</nav>', 1)

    # 2. Inject CSS before </style>
    content = content.replace('</style>', MOBILE_NAV_CSS + '\n</style>', 1)

    # 3. Remove any existing mobile nav hide rules to avoid conflicts
    # (the old pattern was just `display:none` on nav-links in media query)
    content = re.sub(
        r'@media\s*\(max-width:\s*(?:900|960)px\)\s*\{[^}]*\.nav-links\s*\{\s*display:\s*none[^}]*\}',
        '',
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {filepath}")
        total += 1

print(f"\nDone. {total} files updated.")
