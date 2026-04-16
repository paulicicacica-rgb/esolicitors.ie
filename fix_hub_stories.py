import glob
import re
import os

# Map section hub pages to their real story subpages
REAL_STORIES = {
    "./employment-law/index.html": [
        ("/employment-law/unfair-dismissal/james-cork/", "Employment Law", "James, Cork", "Dismissed after 4 years with no process. WRC ruled in his favour.", "WRC ruling — compensation awarded"),
        ("/employment-law/redundancy/claire-dublin/", "Employment Law", "Claire, Dublin", "Made redundant but her role was quietly filled by someone else two weeks later.", "Automatically unfair — compensation awarded"),
        ("/employment-law/discrimination/aoife-cork/", "Employment Law", "Aoife, Cork", "Passed over for promotion three times. A male colleague with less experience was chosen each time.", "Discrimination upheld — settlement reached"),
    ],
    "./family-law/index.html": [
        ("/family-law/divorce-ireland/lena-dublin/", "Family Law", "Lena, Dublin", "Married 14 years. Wanted a clean break but was worried about the family home and pension.", "Divorce finalised — fair division agreed"),
        ("/family-law/child-custody/ciara-cork/", "Family Law", "Ciara, Cork", "Separated from her partner. Wanted to ensure her children stayed in the same school.", "Custody arrangement confirmed"),
        ("/family-law/domestic-violence/fatima-dublin/", "Family Law", "Fatima, Dublin", "Needed to leave quickly and safely. Did not know she could get an emergency barring order the same day.", "Emergency order granted within 24 hours"),
    ],
    "./personal-injury/index.html": [
        ("/personal-injury/dog-bite/aoife-dublin/", "Personal Injury", "Aoife, Dublin", "Bitten by a neighbour's dog in a communal green. Owner said it had never happened before.", "Claim successful — compensation awarded"),
        ("/personal-injury/slip-fall/marek-cork/", "Personal Injury", "Marek, Cork", "Tripped on a broken floor tile in a shopping centre. Missed three weeks of work.", "Compensation awarded including loss of earnings"),
        ("/personal-injury/workplace-injury/blessing-dublin/", "Personal Injury", "Blessing, Dublin", "Injured lifting heavy boxes with no manual handling training. HR said it was part of the job.", "Settled — employer found negligent"),
    ],
    "./property-law/index.html": [
        ("/property-law/landlord-illegal-eviction/oksana-dublin/", "Property Law", "Oksana, Dublin", "Landlord gave her 30 days to leave in January with two children in school nearby.", "Eviction overturned"),
        ("/property-law/deposit-disputes/marta-dublin/", "Property Law", "Marta, Dublin", "Landlord kept her full deposit claiming damage that was already there when she moved in.", "Deposit returned in full"),
        ("/property-law/rent-increase-dispute/wojciech-cork/", "Property Law", "Wojciech, Cork", "Rent increased by 22% with one month's notice. Landlord claimed it was a new tenancy.", "RTB ruled in tenant's favour"),
    ],
    "./criminal-law/index.html": [
        ("/criminal-law/drink-driving-ireland/", "Criminal Law", "Ronan, Dublin", "Stopped at a checkpoint just over the limit. Faced losing his licence and his job.", "Charge struck out — licence retained"),
        ("/criminal-law/no-insurance-ireland/", "Criminal Law", "Patrick, Cork", "Driving his partner's car not knowing he wasn't covered. Faced a mandatory disqualification.", "Penalty points only — disqualification avoided"),
        ("/criminal-law/garda-interview-rights/ronan-dublin/", "Criminal Law", "Ronan, Dublin", "Brought in for questioning. Did not know he had the right to a solicitor before saying anything.", "Released without charge"),
    ],
    "./immigration-law/index.html": [
        ("/immigration-law/visa-refusal-appeal/kwame-cork/", "Immigration Law", "Kwame, Cork", "Visa refused with no clear reason given. Had been living and working in Ireland for 6 years.", "Appeal successful — visa granted"),
        ("/immigration-law/deportation-order/yemi-cork/", "Immigration Law", "Yemi, Cork", "Received a deportation order after a missed renewal. Had Irish-born children.", "Order revoked — leave to remain granted"),
        ("/immigration-law/family-reunification/fatima-dublin/", "Immigration Law", "Fatima, Dublin", "Trying to bring her mother to Ireland after years apart. Every application was refused.", "Reunification approved on appeal"),
    ],
    "./wills-probate/index.html": [
        ("/wills-probate/contesting-a-will/patricia-cork/", "Wills & Probate", "Patricia, Cork", "Her father's will left everything to one sibling. She believed he lacked capacity when he signed it.", "Settlement negotiated — fair share received"),
        ("/wills-probate/making-a-will/john-dublin/", "Wills & Probate", "John, Dublin", "Put off making a will for years. A health scare made him realise what could happen to his family.", "Will completed — family protected"),
        ("/wills-probate/probate-process/anne-dublin/", "Wills & Probate", "Anne, Dublin", "Her husband died without a will. She did not know she needed probate just to access their joint account.", "Probate granted — estate settled"),
    ],
}

STORY_SECTION_PATTERNS = [
    # Pattern 1: stories-grid with story-card links
    re.compile(r'<div class="stories-grid">.*?</div>\s*</section>', re.DOTALL),
    # Pattern 2: section with class containing "stories" or "real"
    re.compile(r'<section[^>]*(?:stories|real-sit)[^>]*>.*?</section>', re.DOTALL | re.IGNORECASE),
]

def build_stories_html(stories):
    cards = []
    for url, tag, name, excerpt, outcome in stories:
        # Only link if page exists
        path = '.' + url.rstrip('/') + '/index.html'
        if not os.path.exists(path):
            # Try without trailing slash index
            path2 = '.' + url.rstrip('/')
            if not os.path.exists(path2):
                print(f"  Warning: {path} not found, linking anyway")
        
        cards.append(f'''      <a href="{url}" class="story-card">
        <span class="story-tag">{tag}</span>
        <div class="story-title">"{excerpt}"</div>
        <div class="story-meta">
          <span class="story-person">{name}</span>
          <span class="story-outcome">✓ {outcome}</span>
        </div>
        <span class="story-read">Read {name.split(",")[0]}\'s story →</span>
      </a>''')
    
    return f'''<section class="stories-section" id="stories">
  <div style="max-width:1200px;margin:0 auto;padding:0 5%">
    <div class="section-label" style="color:var(--gold-light,#e8b04a)">Real Situations</div>
    <h2 class="section-title" style="color:#fff">What happened to people just like you</h2>
    <p class="section-sub" style="color:rgba(255,255,255,0.5)">These situations are more common than you think. You are not alone — and there is help.</p>
    <div class="stories-grid">
{chr(10).join(cards)}
    </div>
  </div>
</section>'''

updated = 0

for filepath, stories in REAL_STORIES.items():
    if not os.path.exists(filepath):
        print(f"Hub not found: {filepath}")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Find and replace the stories section
    # Look for stories-grid or stories-section
    new_section = build_stories_html(stories)

    replaced = False
    for pattern in STORY_SECTION_PATTERNS:
        match = pattern.search(content)
        if match:
            content = content[:match.start()] + new_section + content[match.end():]
            replaced = True
            print(f"  Replaced stories section: {filepath}")
            break

    if not replaced:
        # No stories section found — inject before footer
        if '<footer' in content:
            content = content.replace('<footer', new_section + '\n<footer', 1)
            print(f"  Injected stories section: {filepath}")
        else:
            print(f"  Could not find injection point: {filepath}")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1

print(f"\nDone. Updated {updated} hub pages.")
