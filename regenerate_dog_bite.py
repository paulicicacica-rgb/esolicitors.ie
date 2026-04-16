import os, json, re, time, urllib.request, urllib.error

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

SYSTEM = "You write short story pages for eSolicitors.ie. Write complete HTML. Plain warm English. Tell the story in 3-4 paragraphs. One section on Irish law. One warning box on time limits. No similar cases, no contact info, no phone numbers. Use CSS variables: --navy:#0c1f3d --gold:#c8922a --cream:#f7f3ee. Include nav with eSolicitors.ie branding. Output ONLY valid HTML, no markdown, no backticks."

CTA = '\n<div style="background:#0c1f3d;padding:60px 5%;text-align:center"><div style="max-width:600px;margin:0 auto"><div style="font-size:.75rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#c8922a;margin-bottom:12px">Free Solicitor Matching</div><h2 style="font-family:\'Playfair Display\',serif;font-size:1.8rem;font-weight:700;color:#fff;margin-bottom:14px">Sound familiar? You may have a case too.</h2><p style="color:rgba(255,255,255,0.6);font-size:.95rem;margin-bottom:32px">Tell Sarah what happened. Free, confidential, no obligation.</p></div><div style="max-width:480px;margin:0 auto"><script src="/sarah.js" data-mode="inline"></script></div></div>\n<footer style="background:#080f1e;padding:36px 5%;font-family:\'DM Sans\',sans-serif"><div style="max-width:1100px;margin:0 auto;display:flex;flex-wrap:wrap;justify-content:space-between;gap:32px;margin-bottom:28px"><a href="/" style="font-family:\'Playfair Display\',serif;font-size:1.2rem;font-weight:700;color:#fff;text-decoration:none">e<span style="color:#c8922a">Solicitors</span>.ie</a><ul style="list-style:none;display:flex;flex-direction:column;gap:8px"><li><a href="/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Home</a></li><li><a href="/personal-injury/" style="color:rgba(255,255,255,0.35);text-decoration:none;font-size:.83rem">Personal Injury</a></li></ul></div><div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:18px"><span style="font-size:.75rem;color:rgba(255,255,255,0.25)">2026 eSolicitors.ie</span></div></footer>\n</body></html>'

MISSING = [
    {"path": "./personal-injury/dog-bite/aoife-dublin/index.html", "hub_url": "/personal-injury/dog-bite/", "hub_label": "Dog Bite Claims Ireland", "name": "Aoife", "location": "Dublin", "situation": "Bitten by a neighbour's dog that had slipped its lead in a communal green. The owner insisted the dog had never done anything like this before.", "outcome": "Claim successful — compensation awarded", "law": "Control of Dogs Act 1986 — strict liability applies regardless of prior behaviour", "time_limit": "2 years from the date of the incident"},
    {"path": "./personal-injury/dog-bite/tomas-galway/index.html", "hub_url": "/personal-injury/dog-bite/", "hub_label": "Dog Bite Claims Ireland", "name": "Tomas", "location": "Galway", "situation": "A gas meter reader bitten on a routine visit. His employer told him it was his own fault for not reading the warning signs properly.", "outcome": "Settlement included loss of earnings", "law": "Control of Dogs Act 1986 — strict liability applies regardless of prior behaviour", "time_limit": "2 years from the date of the incident"},
    {"path": "./personal-injury/dog-bite/blessing-limerick/index.html", "hub_url": "/personal-injury/dog-bite/", "hub_label": "Dog Bite Claims Ireland", "name": "Blessing", "location": "Limerick", "situation": "Knocked to the ground and bitten by a large dog that broke free from its owner during a walk. Sustained bruising and a deep bite on her calf.", "outcome": "Psychological impact included in award", "law": "Control of Dogs Act 1986 — strict liability applies regardless of prior behaviour", "time_limit": "2 years from the date of the incident"},
    {"path": "./personal-injury/dog-bite/piotr-kildare/index.html", "hub_url": "/personal-injury/dog-bite/", "hub_label": "Dog Bite Claims Ireland", "name": "Piotr", "location": "Kildare", "situation": "Delivery driver bitten at a rural property. The dog had been in the garden unattended. The owner had no home insurance but the claim still proceeded.", "outcome": "Full settlement reached", "law": "Control of Dogs Act 1986 — strict liability applies regardless of prior behaviour", "time_limit": "2 years from the date of the incident"},
    {"path": "./personal-injury/workplace-injury/blessing-dublin/index.html", "hub_url": "/personal-injury/workplace-injury/", "hub_label": "Workplace Injury Claims Ireland", "name": "Blessing", "location": "Dublin", "situation": "Warehouse worker who injured her back lifting heavy boxes without any manual handling training. HR told her it was just part of the job.", "outcome": "Settled — back injury, loss of earnings included", "law": "Safety Health and Welfare at Work Act 2005 — employers must provide safe systems of work and proper training", "time_limit": "2 years from the date of the injury"},
    {"path": "./personal-injury/workplace-injury/sean-cork/index.html", "hub_url": "/personal-injury/workplace-injury/", "hub_label": "Workplace Injury Claims Ireland", "name": "Sean", "location": "Cork", "situation": "Construction worker who fell from scaffolding. No safety harness had been provided. His employer claimed he should have requested one.", "outcome": "Full compensation — employer found negligent", "law": "Safety Health and Welfare at Work Act 2005 — employers must provide safety equipment", "time_limit": "2 years from the date of the injury"},
    {"path": "./personal-injury/workplace-injury/miroslava-galway/index.html", "hub_url": "/personal-injury/workplace-injury/", "hub_label": "Workplace Injury Claims Ireland", "name": "Miroslava", "location": "Galway", "situation": "Slipped on a wet kitchen floor where no non-slip footwear had been provided despite repeated requests. Fractured her ankle.", "outcome": "Compensation awarded including future losses", "law": "Safety Health and Welfare at Work Act 2005 — employers must maintain safe premises", "time_limit": "2 years from the date of the injury"},
    {"path": "./personal-injury/workplace-injury/thomas-kildare/index.html", "hub_url": "/personal-injury/workplace-injury/", "hub_label": "Workplace Injury Claims Ireland", "name": "Thomas", "location": "Kildare", "situation": "Factory worker whose hand was caught in machinery that lacked a proper safety guard. The guard had been removed weeks earlier for maintenance.", "outcome": "Significant settlement — permanent injury", "law": "Safety Health and Welfare at Work Act 2005 — machinery must be properly guarded", "time_limit": "2 years from the date of the injury"},
]

def call_claude(prompt):
    payload = json.dumps({"model": "claude-haiku-4-5-20251001", "max_tokens": 3000, "system": SYSTEM, "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload, headers={"Content-Type": "application/json", "x-api-key": API_KEY, "anthropic-version": "2023-06-01"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        print(f"API error: {e.code}")
        return None

for story in MISSING:
    if os.path.exists(story["path"]):
        print(f"Exists: {story['path']}")
        continue
    print(f"Generating: {story['path']}")
    prompt = f"Write a story page for eSolicitors.ie.\nPerson: {story['name']} from {story['location']}\nSituation: {story['situation']}\nOutcome: {story['outcome']}\nLaw: {story['law']}\nTime limit: {story['time_limit']}\nHub URL: {story['hub_url']}\nAdd a back link after the nav to {story['hub_url']} saying Back to {story['hub_label']}.\nEnd after the time limit warning box. Do not add footer or closing body/html tags."
    html = call_claude(prompt)
    if html:
        html = re.sub(r'^```html\s*', '', html.strip())
        html = re.sub(r'\s*```$', '', html.strip())
        html = re.sub(r'\s*</body>\s*</html>\s*$', '', html).rstrip()
        html = re.sub(r'<script src="/sarah\.js"[^>]*></script>', '', html)
        os.makedirs(os.path.dirname(story["path"]), exist_ok=True)
        with open(story["path"], 'w', encoding='utf-8') as f:
            f.write(html + "\n" + CTA)
        print(f"  Saved: {story['path']}")
        time.sleep(1)
    else:
        print(f"  FAILED: {story['path']}")

print("Done.")
